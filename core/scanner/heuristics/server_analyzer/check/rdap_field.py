from core.models.result_base import ResultBase
from core.scanner.heuristics.server_analyzer.check.domain_age import _resolve_rdap_url
from core.network.config_net import clients

def rdap_metadata_incompleteness(structure: dict) -> ResultBase:
    hostname = structure.get("hostname", "")

    if not hostname:
        return ResultBase(
            value=None,
            normalized=None,
            weight=2.0,
            details={
                "error": "No hostname"
            }
        )

    try:
        rdap_url = _resolve_rdap_url(hostname)
        for client in clients:
            try:
                data = client.get(rdap_url).json()
                break
            except Exception:
                continue
            
        if "errorCode" in data:
            return ResultBase(
                value=None,
                normalized=None,
                weight=0.0,
                details={
                    "error": "Invalid RDAP response"
                }
            )

        fields = [
            data.get("entities"),
            data.get("nameservers"),
            data.get("events"),
        ]

        missing = sum(1 for f in fields if f is None)

        score = missing / len(fields)

        return ResultBase(
            value=missing,
            normalized=score,
            weight=2.8,
            details={
                "missing_fields": missing
            }
        )

    except Exception:
        return ResultBase(
            value=None,
            normalized=None,
            weight=0.5,
            details={
                "error": "RDAP lookup failed"
            }
        )