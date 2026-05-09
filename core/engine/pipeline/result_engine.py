from time import time
from core.models.scan_context import ScanContext
from core.engine.analysis.insights import insights
from __init__ import __version__

def build_error_response(ctx: ScanContext, error_type: str, message: str) -> dict:
    return {
        "status": "error",
        "meta": {
            "url": ctx.url,
            "scan_time_s": round(time() - ctx.meta.start, 3),
            "version": __version__
        },
        "error": {
            "type": error_type,
            "message": message
        }
    }

def build_response(ctx: ScanContext, rules_total: int) -> dict:
    rules_triggered = len(ctx.heuristics)
    now = time()

    return {
        "status": "ok",
        "engine": {
            "name": "scurl",
            "version": __version__
        },
        "meta": {
            "scan_id": ctx.scan_id,
            "scan_time_s": round(time() - ctx.meta.start, 3),
            "url_hash": ctx.url_hash,
            "threads": ctx.threads,
            "timestamp": ctx.timestamp
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
            "is_https": ctx.structure.get("scheme") == "https"
        },
        "network": {
            "status_code": ctx.response.status if ctx.response else None,
            "response_time_s": round(ctx.response.elapsed, 3) if ctx.response else None
        },
        "raw": {
            "size_kb": ctx.size,
            "headers": dict(ctx.response.headers) if ctx.response else None,
            "redirects": ctx.response.redirects if ctx.response else None,
            "chain": ctx.response.redirect_chain if ctx.response else None
        },
        "stats": {
            "rules_total": rules_total,
            "rules_triggered": rules_triggered,
            "trigger_rate": round(rules_triggered / rules_total, 3) if rules_total else 0
        },
        "heuristics": ctx.heuristics,
        "insight": insights(ctx.heuristics, ctx.score)
    }