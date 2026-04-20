from core.models.scan_rule import ScanRule
from core.models.scan_result import ScanResult
from core.scanner.heuristics.url_analyzer.check.character_check import hyphen_risk, at_risk, equal_risk, num_ratio_risk, mixed_encoding, xss_risk
from core.engine.rule_registry import register

@register
class HyphenRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="hyphen_risk", category="url", severity="medium")

    def run(self, context):
        data = hyphen_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)

@register
class AtRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="at_risk", category="url", severity="high")

    def run(self, context):
        data = at_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)

@register
class EqualRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="equal_risk", category="url", severity="medium")

    def run(self, context):
        data = equal_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)

@register
class NumRatioRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="num_ratio_risk", category="url", severity="medium")

    def run(self, context):
        data = num_ratio_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)

@register
class MixEncodingRule(ScanRule):
    def __init__(self):
        super().__init__(name="mix_encoding", category="url", severity="medium")

    def run(self, context):
        data = mixed_encoding(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)

@register
class XSSPatternRule(ScanRule):
    def __init__(self):
        super().__init__(name="xss_pattern", category="url", severity="high")

    def run(self, context):
        data = xss_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, details=data.details, severity=self.severity)