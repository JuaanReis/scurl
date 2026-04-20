from core.models.scan_context import ScanContext
from core.engine.pipeline import (
    validate_target,
    collect_target_data,
    execute_rules,
    calculate_score,
    build_response,
    build_error_response,
)
from core.scanner.heuristics.response_analyzer.rules.response_rules import (
    ExternalScriptRule, FaviconRule, FormActionRule, HiddenFieldsRule,
    ImageSrcRule, PasswordInputRule, RedirectRule
)
from core.scanner.heuristics.server_analyzer.rules.server_rules import (
    DNSVerifyRule, DomainAgeRule, SSLVerifyRule,
    RDAPFieldIncompletenessRule, NameServerDiversityRule
)
from core.scanner.heuristics.url_analyzer.rules.character_rules import (
    AtRiskRule, EqualRiskRule, HyphenRiskRule,
    MixEncodingRule, NumRatioRiskRule, XSSPatternRule
)
from core.scanner.heuristics.url_analyzer.rules.domain_rules import (
    IPInURLRule, RandomDomainRiskRule, RandomSubdomainRiskRule, SubdomainCountRule
)
from core.scanner.heuristics.url_analyzer.rules.parts_rules import (
    Base64SegmentRule, FragmentRiskRule, PathDepthRiskRule,
    QueryContainsURLRule, QueryNoValueRule, RandomPathRiskRule
)

RULES = [
    SSLVerifyRule, DomainAgeRule, DNSVerifyRule, RDAPFieldIncompletenessRule, NameServerDiversityRule,
    NumRatioRiskRule, MixEncodingRule, AtRiskRule, HyphenRiskRule, EqualRiskRule, XSSPatternRule,
    RandomPathRiskRule, QueryNoValueRule, QueryContainsURLRule, Base64SegmentRule, PathDepthRiskRule, FragmentRiskRule,
    IPInURLRule, SubdomainCountRule, RandomDomainRiskRule, RandomSubdomainRiskRule,
    ExternalScriptRule, FaviconRule,
    RedirectRule, HiddenFieldsRule, ImageSrcRule, PasswordInputRule, FormActionRule
]

def run_engine(url: str, processors: int = 2) -> dict:
    ctx = ScanContext(url)

    if error := validate_target(ctx):
        return error

    if error := collect_target_data(ctx):
        return error

    rules = [rule() for rule in RULES]
    
    if error := execute_rules(ctx, rules, processors):
        return build_error_response(ctx, **error["error"])

    calculate_score(ctx)
    return build_response(ctx, rules_total=len(rules))