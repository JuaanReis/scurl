from uuid import uuid4
from __init__ import __version__
from time import time 
from datetime import UTC, datetime 
from core.engine.context_aply import apply_dependencies
from .classification import classify
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout, as_completed
from core.scanner.heuristics.response_analyzer.rules.response_rules import ExternalScriptRule, FaviconRule, FormActionRule, HiddenFieldsRule, ImageSrcRule, ParseHtmlResponseRule, PasswordInputRule, RedirectRule
from core.scanner.heuristics.server_analyzer.rules.server_rules import DNSVerifyRule, DomainAgeRule, SSLVerifyRule, RDAPFieldIncompletenessRule, NameServerDiversityRule
from core.scanner.heuristics.url_analyzer.rules.character_rules import AtRiskRule, EqualRiskRule, HyphenRiskRule, MixEncodingRule, NumRatioRiskRule, XSSPatternRule
from core.scanner.heuristics.url_analyzer.rules.domain_rules import IPInURLRule, RandomDomainRiskRule, RandomSubdomainRiskRule, SubdomainCountRule
from core.scanner.heuristics.url_analyzer.rules.parts_rules import Base64SegmentRule, FragmentRiskRule, PathDepthRiskRule, QueryContainsURLRule, QueryNoValueRule, RandomPathRiskRule
from core.scanner.score.sigmoid import sigmoid
from .insights import insights
from .url_extract.get_structure import get_structure
from .url_validator import url_validator, response_validator

RULES = [
    SSLVerifyRule, DomainAgeRule, DNSVerifyRule, RDAPFieldIncompletenessRule, NameServerDiversityRule,
    NumRatioRiskRule, MixEncodingRule, AtRiskRule, HyphenRiskRule, EqualRiskRule, XSSPatternRule,
    RandomPathRiskRule, QueryNoValueRule, QueryContainsURLRule, Base64SegmentRule, PathDepthRiskRule, FragmentRiskRule,
    IPInURLRule, SubdomainCountRule, RandomDomainRiskRule, RandomSubdomainRiskRule,
    ExternalScriptRule, FaviconRule, ImageSrcRule,
    RedirectRule, HiddenFieldsRule, PasswordInputRule, FormActionRule
]

MAX_SCAN_SECONDS = 15

def run_engine(url: str, processors: int = 2) -> dict:
    error = url_validator.url_validator(url)
    if error:
        return error

    start = time()
    try:
        structure, response = get_structure(url)
        error = response_validator.response_validator(response, url, start)

        if error:
            return error

        scores, weights = [], []
        
        results_map: dict[str, float | None] = {}
        heuristics = []
        rules = [rule() for rule in RULES]

        with ThreadPoolExecutor(max_workers=min(processors, 8)) as executor:
            futures = [executor.submit(rule.run, structure) for rule in rules]
            results = []
            for future in as_completed(futures, timeout=MAX_SCAN_SECONDS):
                try:
                    results.append(future.result())
                except FuturesTimeout:
                    return {
                        "status": "error",
                        "meta": {
                            "url": url,
                            "scan_time_s": round(time() - start, 3),
                            "version": __version__
                        },
                        "error": {
                            "type": "scan_timeout",
                            "message": "Scan excedeu o tempo limite"
                        }
                    }

        for result in results:
            results_map[result.name] = result.value

        for result in results:
            adj_value, adj_weight, dep_reasons = apply_dependencies(
                result.name,
                result.value,
                result.weight,
                results_map
            )

            if adj_value is not None:
                scores.append(adj_value)
                weights.append(adj_weight)

            if adj_value is not None and adj_value > 0:
                heuristics.append({
                    "name": result.name,
                    "category": result.category,
                    "value": round(adj_value, 2),
                    "weight": round(adj_weight, 2),
                    "contribution": round(adj_value * adj_weight, 1),
                    "details": result.details,
                    "reasons": dep_reasons
                })

        score = sigmoid(scores, weights)
        classification, risk = classify(score)

        return {
            "status": "ok",
            "engine": {
                "name": "scurl",
                "version": __version__
            },
            "meta": {
                "scan_id": uuid4().hex,
                "scan_time_s": round(time() - start, 3),
                "timestamp": datetime.fromtimestamp(time(), UTC).isoformat()
            },
            "result": {
                "score": round(score, 2),
                "risk_level": risk,
                "verdict": classification,
            },
            "target": {
                "url": structure.get("url", ""),
                "scheme": structure.get("scheme", ""),
                "hostname": structure.get("hostname", ""),
                "registered_domain": structure.get("registered_domain", ""),
                "tld": structure.get("tld", ""),
                "subdomains": structure.get("subdomain", []),
                "subdomain_count": structure.get("subdomain_count", 0),
                "netloc": structure.get("netloc", ""),
                "is_https": structure.get("scheme") == "https"
            },
            "network": {
                "status_code": response.status,
                "response_time_s": response.elapsed
            },
            "stats": {
                "rules_total": len(rules),
                "rules_triggered": len(heuristics),
                "trigger_rate": len(heuristics) / len(rules) if len(rules) > 0 else 0
            },
            "heuristics": heuristics,
            "insight": insights(heuristics, score)
        }
    
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "meta": {
                "url": url, 
                "scan_time_s": round(time() - start, 3),
                "version": __version__
            },
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "trace": traceback.format_exc()
            }
        }