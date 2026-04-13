from time import time 
from datetime import datetime, timezone
from core.engine.context_aply import apply_dependencies
from core.scanner.heuristics.response_analyzer.rules.response_rules import ExternalScriptRule, FaviconRule, FormActionRule, HiddenFieldsRule, ImageSrcRule, ParseHtmlResponseRule, PasswordInputRule, RedirectRule
from core.scanner.heuristics.server_analyzer.rules.server_rules import DNSVerifyRule, DomainAgeRule, SSLVerifyRule
from core.scanner.heuristics.url_analyzer.rules.character_rules import AtRiskRule, EqualRiskRule, HyphenRiskRule, MixEncodingRule, NumRatioRiskRule, XSSPatternRule
from core.scanner.heuristics.url_analyzer.rules.domain_rules import IPInURLRule, RandomDomainRiskRule, RandomSubdomainRiskRule, SubdomainCountRule
from core.scanner.heuristics.url_analyzer.rules.parts_rules import Base64SegmentRule, FragmentRiskRule, PathDepthRiskRule, QueryContainsURLRule, QueryNoValueRule, RandomPathRiskRule
from core.scanner.heuristics.url_analyzer.url_structure import extract_structure
from core.scanner.score.sigmoid import sigmoid

def _classify(score: float) -> tuple[str, str]:
    if score < 20:
        return "safe", "low"
    if score < 45:
        return "suspicious", "medium"
    if score < 70:
        return "dangerous", "high"
    return "malicious", "critical"

def run_engine(url: str) -> dict:
    if not url:
        return {
            "status": "error",
            "meta": {
                "url": None,
                "scan_time_s": 0,
                "version": "0.1"
            },
            "error": {
                "type": "missing_url",
                "message": "URL não informada"
            }
        }
    
    if not url.startswith(("http://", "https://")):
        return {
            "status": "error",
            "meta": {
                "url": url,
                "scan_time_s": 0,
                "version": "0.1"
            },
            "error": {
                "type": "missing_protocol",
                "message": "URL inválida"
            }
        }

    start = time()

    try:
        structure = extract_structure(url) or {}
        body_result = ParseHtmlResponseRule().run(structure)
        structure["html_parser"] = body_result.response 

        rules = [
            SSLVerifyRule(), DomainAgeRule(), DNSVerifyRule(),
            NumRatioRiskRule(), MixEncodingRule(), AtRiskRule(), HyphenRiskRule(), EqualRiskRule(), XSSPatternRule(),
            RandomPathRiskRule(), QueryNoValueRule(), QueryContainsURLRule(), Base64SegmentRule(), PathDepthRiskRule(), FragmentRiskRule(),
            IPInURLRule(), SubdomainCountRule(), RandomDomainRiskRule(), RandomSubdomainRiskRule(),
            ExternalScriptRule(), FaviconRule(), ImageSrcRule(),
            RedirectRule(), HiddenFieldsRule(), PasswordInputRule(), FormActionRule()
        ]

        scores = []
        weights = []
        results_map: dict[str, float | None] = {}
        raw_results = []

        for rule in rules:
            result = rule.run(structure)
            raw_results.append(result)
            results_map[result.name] = result.value

        heuristics = []

        for result in raw_results:
            adj_value, adj_weight, dep_reasons = apply_dependencies(
                result.name, result.value, result.weight, results_map
            )

            scores.append(adj_value)
            weights.append(adj_weight)

            if adj_value is not None and adj_value > 0:
                heuristics.append({
                    "name": result.name,
                    "category": result.category,
                    "value": round(adj_value, 2),
                    "weight": round(adj_weight, 2),
                    "details": result.details,
                    "reasons": dep_reasons
                })

        score = sigmoid(scores, weights)
        classification, risk = _classify(score)

        return {
            "status": "ok",
            "engine": {
                "name": "scurl",
                "version": "0.1"
            },
            "meta": {
                "url": url,
                "scan_time_s": round(time() - start, 3),
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "result": {
                "score": round(score, 2),
                "risk_level": risk,
                "verdict": classification,
            },
            "stats": {
                "rules_total": len(raw_results),
                "rules_triggered": len(heuristics)
            },
            "heuristics": heuristics
        }
    
    except Exception as e:
        return {
            "status": "error",
            "meta": {
                "url": url, 
                "scan_time_s": round(time() - start, 3), 
                "version": "0.1"
            },
            "error": {
                "type": type(e).__name__, 
                "message": str(e)
            }
        }