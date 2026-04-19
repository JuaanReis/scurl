from core.models.result_base import ResultBase
from core.scanner.heuristics.server_analyzer.check.domain_age import _resolve_rdap_url
from core.network.config_net import clients
import tldextract

def nameserver_diversity(structure: dict) -> ResultBase:
    hostname = structure.get("hostname")

    if not hostname:
        return ResultBase(
            value=None,
            normalized=None,
            weight=3.0,
            details={"error": "No hostname"}
        )

    try:
        rdap_url = _resolve_rdap_url(hostname)

        data = None
        for client in clients:
            try:
                resp = client.get(rdap_url, timeout=5)
                data = resp.json()
                break
            except Exception:
                continue

        if not data:
            raise RuntimeError("RDAP lookup failed")

        nameservers = data.get("nameservers") or []

        if not nameservers:
            return ResultBase(
                value=0,
                normalized=1.0,
                weight=3.0,
                details={"unique_ns_domains": 0, "nameserver_count": 0}
            )

        domains = set()

        for ns in nameservers:
            name = ns.get("ldhName")
            if not name:
                continue

            ext = tldextract.extract(name)

            if ext.domain and ext.suffix:
                domains.add(f"{ext.domain}.{ext.suffix}")

        ns_count = len(nameservers)
        unique_domains = len(domains)

        diversity_ratio = unique_domains / ns_count

        if ns_count == 1:
            score = 0.9
        elif ns_count == 2 and diversity_ratio == 1:
            score = 0.6
        elif diversity_ratio > 0.8:
            score = 0.5
        else:
            score = 0.0

        return ResultBase(
            value=unique_domains,
            normalized=score,
            weight=3.0,
            details={
                "unique_ns_domains": unique_domains,
                "nameserver_count": ns_count,
                "diversity_ratio": round(diversity_ratio, 2)
            }
        )

    except Exception:
        return ResultBase(
            value=None,
            normalized=None,
            weight=3.0,
            details={"error": "RDAP lookup failed"}
        )