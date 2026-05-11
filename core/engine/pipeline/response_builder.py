from time import time
from core.models.scan_context import ScanContext
from core.engine.analysis.insights import insights
from importlib.metadata import version
__version__ = version("scurl")

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

def build_target(ctx: ScanContext) -> dict:
    structure = ctx.target.structure
    response = ctx.target.response

    return {
        "url": structure.get("url", ""),
        "scheme": structure.get("scheme", ""),
        "hostname": structure.get("hostname", ""),
        "registered_domain": structure.get("registered_domain", ""),
        "tld": structure.get("tld", ""),
        "subdomains": structure.get("subdomain", []),
        "subdomain_count": structure.get("subdomain_count", 0),
        "is_https": structure.get("scheme") == "https",
        "network": {
            "status_code": response.status if response else None,
            "response_time_s": round(response.elapsed, 3) if response else None
        },
        "raw": {
            "size_kb": ctx.target.size_kb,
            "headers": dict(response.headers) if response else None,
            "redirects": response.redirects if response else None,
            "chain": response.redirect_chain if response else None
        }
    }

def build_scan(ctx: ScanContext, rules_total: int) -> dict:
    rules_triggered = len(ctx.heuristics)

    return {
        "status": "ok",
        "engine": {
            "name": "scurl",
            "version": __version__
        },
        "meta": {
            "scan_id": ctx.meta.scan_id,
            "scan_time_s": round(time() - ctx.meta.start, 3),
            "url_hash": ctx.meta.url_hash,
            "threads": ctx.meta.threads,
            "timestamp": ctx.meta.timestamp.isoformat()
        },
        "result": {
            "score": round(ctx.score, 2),
            "risk_level": ctx.risk,
            "verdict": ctx.classification,
        },
        "stats": {
            "rules_total": rules_total,
            "rules_triggered": rules_triggered,
            "trigger_rate": round(rules_triggered / rules_total, 3) if rules_total else 0
        },
        "heuristics": ctx.heuristics,
        "insight": insights(ctx.heuristics, ctx.score)
    }

def build_response(ctx: ScanContext, rules_total: int) -> tuple[dict, dict]:
    return build_scan(ctx, rules_total), build_target(ctx)