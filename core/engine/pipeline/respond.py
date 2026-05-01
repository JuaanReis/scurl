from uuid import uuid4
from time import time
from datetime import UTC, datetime
from core.models.scan_context import ScanContext
from core.engine.analysis.insights import insights
from __init__ import __version__

def build_error_response(ctx: ScanContext, error_type: str, message: str) -> dict:
    return {
        "status": "error",
        "meta": {
            "url": ctx.url,
            "scan_time_s": round(time() - ctx.start, 3),
            "version": __version__
        },
        "error": {
            "type": error_type,
            "message": message
        }
    }

def build_response(ctx: ScanContext, rules_total: int) -> dict:
    rules_triggered = len(ctx.heuristics)

    return {
        "status": "ok",
        "engine": {
            "name": "scurl",
            "version": __version__
        },
        "meta": {
            "scan_id": uuid4().hex,
            "scan_time_s": round(time() - ctx.start, 3),
            "timestamp": datetime.fromtimestamp(time(), UTC).isoformat()
        },
        "result": {
            "score": round(ctx.score, 2),
            "risk_level": ctx.risk,
            "verdict": ctx.classification,
        },
        "target": {
            "url": ctx.structure.get("url", ""),
            "scheme": ctx.structure.get("scheme", ""),
            "hostname": ctx.structure.get("hostname", ""),
            "registered_domain": ctx.structure.get("registered_domain", ""),
            "tld": ctx.structure.get("tld", ""),
            "subdomains": ctx.structure.get("subdomain", []),
            "subdomain_count": ctx.structure.get("subdomain_count", 0),
            "netloc": ctx.structure.get("netloc", ""),
            "is_https": ctx.structure.get("scheme") == "https"
        },
        "network": {
            "status_code": ctx.response.status,
            "response_time_s": ctx.response.elapsed
        },
        "stats": {
            "rules_total": rules_total,
            "rules_triggered": rules_triggered,
            "trigger_rate": rules_triggered / rules_total if rules_total > 0 else 0
        },
        "heuristics": ctx.heuristics,
        "insight": insights(ctx.heuristics, ctx.score)
    }