from datetime import datetime, timezone
from core.models.result_base import ResultBase
from core.scanner.score.sigmoid import sigmoid
from .math import f_age, f_valid, f_san, f_wild, f_issuer, f_mismatch, f_self_signed, f_expired, f_org
from .info_ssl import get_ssl_cert

def ssl_score(structure: dict) -> ResultBase:
    """
        Verifica a validade e segurança do certificado SSL do servidor, considerando fatores como idade, validade, SANs, emissor e correspondência de hostname. 
            - Idade do certificado: Certificados muito antigos podem indicar falta de manutenção.
            - Validade: Certificados com validade curta podem ser menos confiáveis.
            - SANs: A presença de Subject Alternative Names pode indicar um certificado mais robusto.
            - Emissor: Certificados emitidos por autoridades confiáveis são mais seguros.
            - Correspondência de hostname: Certificados que não correspondem ao hostname do servidor são um grande sinal de alerta.
        
        A pontuação é calculada usando uma função sigmoidal que combina esses fatores, resultando em um valor normalizado entre 0 e 1, onde valores mais altos indicam um certificado SSL mais confiável e seguro.  
    """

    ssl_data = get_ssl_cert(structure)

    if ssl_data.get("connection_refused", False):
        return ResultBase (
            value = None,
            normalized = 0.65,
            weight = 5.0,
            details = {
                "error": "Connection refused or SSL not supported"
            }
        )

    if ssl_data.get("timeout", False):
        return ResultBase (
            value = None,
            normalized = 0.0,
            weight = 5.0,
            details = {
                "error": "Connection timed out while retrieving SSL certificate"
            }
        )
    
    if ssl_data.get("invalid_cert", False):
        return ResultBase (
            value = None,
            normalized = 0.9,
            weight = 5.0,
            details = {
                "error": "Invalid SSL certificate"
            }
        )

    if ssl_data.get("unknown", False):
        return ResultBase (
            value = None,
            normalized = None,
            weight = 5.0,
            details = {
                "error": "Unknown error while retrieving SSL certificate"
            }
        )

    try:
        issued = datetime.strptime(
            ssl_data["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)

        expire = datetime.strptime(
            ssl_data["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)

    except Exception:
        return ResultBase (
            value = None,
            normalized = 0.5,
            weight = 5.0,
            details = {
                "error": "Invalid SSL date format"
            }
        )

    now = datetime.now(timezone.utc)

    age_days = (now - issued).days
    validity_days = (expire - issued).days
    issuer = ssl_data.get("issuer", {}).get("commonName", "")
    san = ssl_data.get("san", [])

    hostname_valid = ssl_data.get("hostname_valid", True)

    score = [
        [
            f_age(age_days),
            f_valid(validity_days),
            f_san(len(san)),
            f_wild(san),
            f_issuer(issuer),
            f_mismatch(not hostname_valid),
            f_self_signed(ssl_data.get("self_signed", False)),
            f_expired(expire < now),
            f_org(ssl_data.get("organization", ""))
        ],
        [
            1.5, 
            1.0,
            0.5, 
            0.5, 
            0.25, 
            1.0, 
            1.0, 
            1.5,  
            0.5 
        ]
    ]

    f_score = sigmoid(score[0], score[1]) / 100 if sum(score[1]) > 0 else 0.0

    return ResultBase (
        value = f_score,
        normalized = f_score,
        weight = 3.5,
        details = {
            "age_days": age_days,
            "validity_days": validity_days,
            "san_count": len(san),
            "issuer": issuer,
            "hostname_valid": hostname_valid,
            "self_signed": ssl_data.get("self_signed", False)
        }
    )