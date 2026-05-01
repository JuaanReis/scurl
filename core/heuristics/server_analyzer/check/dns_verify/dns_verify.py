from .math import check_dkim_selectors, dns_mx, dns_ttl, dns_a, dns_dkim, dns_spf, get_stable_ttl
from .info_dns import get_dns_info
from core.models.result_base import ResultBase
from core.math.sigmoid import sigmoid

def dns_score(structure: dict) -> ResultBase:
    hostname = structure.get("hostname", "")

    if not hostname:
        return ResultBase(
            value = None, 
            normalized = 0.5, 
            weight = 0.0,
            details = {
                "error": "No hostname provided"
            }
        )

    dns_data = get_dns_info(hostname)

    if dns_data.get("failed", False):
        return ResultBase(
            value=None,
            normalized=1.0,
            weight=3.5,
            details={
                "error": "DNS resolution failed",
                "dns_failed": True
            }
        )

    has_mx = dns_data.get("has_mx")
    ttl = get_stable_ttl(hostname)
    ips = dns_data.get("ips", [])
    txt = dns_data.get("txt", [])

    has_dkim_via_selector = check_dkim_selectors(hostname) if has_mx else False

    scores = [
        dns_mx(has_mx),
        dns_ttl(ttl, has_mx=has_mx),
        dns_a(ips, ttl=ttl),
        dns_spf(txt, has_mx=has_mx),
        dns_dkim(txt, has_mx=has_mx, dkim_found=has_dkim_via_selector)
    ]

    values = [r.normalized for r in scores]
    weights = [r.weight for r in scores]

    score = sigmoid(values, weights, k=5) / 100 if sum(weights) > 0 else 0.0

    return ResultBase(
        value = sum(v for v in values if v is not None),
        normalized = score,
        weight = 3.5,
        details = {
            "has_mx": dns_data.get("has_mx"),
            "ttl": ttl,
            "ip_count": len(dns_data.get("ips", [])),
            "ips": dns_data.get("ips", []),
            "scores": {
                "mx": values[0],
                "ttl": values[1],
                "a": values[2],
                "spf": values[3],
                "dkim": values[4]
            }
        }
    )