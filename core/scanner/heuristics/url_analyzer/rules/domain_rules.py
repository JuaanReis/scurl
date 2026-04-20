from core.models.scan_rule import ScanRule
from core.models.scan_result import ScanResult
from core.scanner.heuristics.url_analyzer.check.typos.typosquatting import typosquatting
from core.scanner.heuristics.url_analyzer.check.domain_check import subdomain_count, ip_in_url, random_domain_risk, random_subdomain_risk
from core.engine.rule_registry import register

# Não executar
class TyposquattingRule(ScanRule):
    def __init__(self):
        super().__init__(name="typosquatting", category="url", severity="high")

    def run(self, context):
        data = typosquatting(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class IPInURLRule(ScanRule):
    def __init__(self):
        super().__init__(name="ip_in_url", category="url", severity="high")

    def run(self, context):
        data = ip_in_url(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class SubdomainCountRule(ScanRule):
    def __init__(self):
        super().__init__(name="subdomain_count", category="url", severity="medium")

    def run(self, context):
        data = subdomain_count(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class RandomDomainRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="random_domain_risk", category="url", severity="medium")

    def run(self, context):
        data = random_domain_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class RandomSubdomainRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="random_subdomain_risk", category="url", severity="medium")

    def run(self, context):
        data = random_subdomain_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)