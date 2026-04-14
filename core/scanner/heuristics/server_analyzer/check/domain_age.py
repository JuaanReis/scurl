from datetime import datetime, timezone
from whois import whois, exceptions
from core.math.exponential_decay import domain_age_score
from core.models.result_base import ResultBase

def domain_age(structure: dict) -> ResultBase:
    """
        Calcula a idade de um domínio em dias utilizando informações WHOIS.
    
        A função consulta os registros WHOIS do domínio fornecido e obtém
        a data de criação do domínio. A partir dessa data, calcula-se a
        diferença em dias entre a data atual e a data de criação, resultando
        na idade do domínio.
    
        Essa informação é frequentemente utilizada em análises de segurança,
        pois domínios muito recentes são comumente associados a campanhas
        de phishing, spam ou distribuição de malware.
    
        Alguns registros WHOIS podem retornar múltiplas datas de criação.
        Nesse caso, a função utiliza apenas o primeiro valor da lista.
    
        Args:
            url (str): Domínio ou URL que será consultado no serviço WHOIS.
    
        Returns:
            int | None:
                - Número de dias desde a criação do domínio.
                - None caso a informação de criação não esteja disponível
                  ou a consulta WHOIS falhe.
    
        Example:
            >>> domain_age("google.com")
            10000
    
        Observações:
            - A consulta depende de servidores WHOIS externos.
            - Alguns domínios podem não possuir dados públicos de criação.
            - Em caso de erro na consulta WHOIS, a função retorna None.
    """
    
    url = structure.get("hostname", "")

    if not url:
        return ResultBase (
            value = None,
            normalized = 0.5,
            weight = 0.0,
            details = {
                "error": "No URL provided"
            }
        )
    
    try:
        info = whois(url)
        creation = info.creation_date

        if isinstance(creation, list):
            creation = creation[0]

        if creation is None:
            return ResultBase (
                value = None,
                normalized = None,
                weight = 0.0,
                details = {
                    "error": "Creation date not available"
                }
            )

        now = datetime.now(timezone.utc)

        age = now - creation

        score = domain_age_score(age.days)

        return ResultBase (
            value = age.days,
            normalized = score if score > 0.1 else 0.0,
            weight = 4.5,
            details = {
                "creation_date": creation.isoformat(),
                "age_days": age.days
            }
        )
    
    except (exceptions.WhoisError, TimeoutError):
        return ResultBase (
            value = None,
            normalized = None,
            weight = 1.0,
            details = {
                "error": "WHOIS lookup failed"
            }
        )