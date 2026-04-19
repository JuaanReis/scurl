from math import exp, log
from core.models.result_base import ResultBase
import dns.resolver
import statistics

def dns_mx(has_mx: bool) -> ResultBase:
    """
    Avalia risco baseado na ausência de registro MX.
    normalized_score ∈ {0, 1}
    """
    if has_mx is None:
        return ResultBase(
            value=None,
            normalized=None,
            weight=2.0,
            details={"has_mx": None}
        )

    normalized = 0.0 if has_mx else 1.0

    return ResultBase(
        value=normalized,
        normalized=normalized if normalized != 0.0 else None,
        weight=2.0,
        details={"has_mx": has_mx}
    )

def get_stable_ttl(hostname: str, samples: int = 1) -> int:
    ttls = []
    for _ in range(samples):
        try:
            answers = dns.resolver.resolve(hostname, "A")
            ttls.append(answers.rrset.ttl)
        except Exception:
            continue
    return int(statistics.median(ttls)) if ttls else None

def dns_ttl(ttl: int, has_mx: bool = None) -> ResultBase:
    if ttl is None:
        return ResultBase(
            value=None, 
            normalized=0.0,     
            weight=1.5,
            details={
                "ttl": None, 
                "context": "ttl_missing"
            }
        )

    if ttl < 60:
        raw = 1.0
        context = "ttl_very_low"
    elif ttl < 300:
        raw = 0.5
        context = "ttl_low"
    elif ttl <= 3600:
        raw = 0.0   
        context = "ttl_normal"
    else:
        raw = 0.1  
        context = "ttl_high"

    if has_mx is True and ttl < 300:
        normalized = raw * 0.4
        context += "_mx_attenuated"

    elif has_mx is False and ttl < 300:
        normalized = min(raw * 1.2, 1.0)
        context += "_no_mx_amplified"

    else:
        normalized = raw

    return ResultBase(
        value=ttl,
        normalized=round(normalized, 4) if normalized > 0.05 else None,
        weight=1.5,
        details={"ttl": ttl, "context": context}
    )


def dns_a(ips: list, ttl: int = None) -> ResultBase:
    """
    Avalia risco baseado na quantidade de IPs associados ao domínio.
    Cruzamento: muitos IPs + TTL baixo indica rotação ativa de IP (bulletproof hosting).
    normalized_score ∈ [0, 1]
    """
    if not ips:
        return ResultBase(
            value=None,
            normalized=1.0,
            weight=1.5,
            details={"ip_count": 0, "ips": [], "context": "no_ips"}
        )

    count = len(ips)

    if count <= 8:
        base_normalized = None
        context = "ip_count_normal"
    else:
        base_normalized = min(log(count - 1) / log(9), 1.0)
        context = "ip_count_high"

    # Cruzamento: muitos IPs com TTL baixo = rotação ativa, amplifica risco
    if base_normalized is not None and ttl is not None and ttl < 120:
        normalized = min(base_normalized * 1.3, 1.0)
        context = "ip_rotation_suspected"
    else:
        normalized = base_normalized

    return ResultBase(
        value=count,
        normalized=round(normalized, 4) if normalized and normalized > 0.05 else None,
        weight=1.5,
        details={"ip_count": count, "ips": ips, "context": context}
    )

def dns_spf(txt_records: list, has_mx: bool = None) -> ResultBase:
    if not txt_records:
        if has_mx is True:
            normalized = 1.0
            context = "no_txt_but_has_mx"

        else:
            normalized = None
            context = "no_txt_no_mx_neutral"

        return ResultBase(
            value=None, 
            normalized=normalized, 
            weight=1.0,
            details={
                "spf": False, 
                "txt_count": 0, 
                "context": context
            }
        )

    has_spf = any("v=spf1" in r.lower() for r in txt_records)

    if not has_spf and has_mx is True:
        normalized = 1.0
        context = "no_spf_with_mx"
    elif not has_spf and has_mx is False:
        normalized = None
        context = "no_spf_no_mx_neutral"
    else:
        normalized = None
        context = "spf_ok"

    return ResultBase(
        value=int(not has_spf), 
        normalized=normalized, 
        weight=1.0,
        details={
            "spf": has_spf, 
            "txt_count": len(txt_records), 
            "context": context
        }
    )

def dns_dkim(txt_records: list, has_mx: bool = None, dkim_found: bool = False) -> ResultBase:
    has_dkim = dkim_found or any("v=dkim1" in r.lower() for r in txt_records)

    if not has_dkim and has_mx is True:
        normalized = 0.1
        context = "no_dkim_with_mx"
    elif not has_dkim and has_mx is False:
        normalized = None
        context = "no_dkim_no_mx_neutral"
    else:
        normalized = None
        context = "dkim_ok"

    return ResultBase(
        value=int(not has_dkim), 
        normalized=normalized, 
        weight=0.1,
        details={
            "dkim": has_dkim, 
            "context": context
        }
    )

COMMON_SELECTORS = ["google", "default", "mail", "dkim", "k1", "s1", "s2"]

def check_dkim_selectors(hostname: str) -> bool:
    """Tenta seletores DKIM comuns antes de declarar ausência."""
    for selector in COMMON_SELECTORS:
        try:
            dns.resolver.resolve(f"{selector}._domainkey.{hostname}", "TXT")
            return True
        except Exception:
            continue
    return False