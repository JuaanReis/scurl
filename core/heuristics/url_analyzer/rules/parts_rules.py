from core.models.scan_rule import ScanRule 
from core.models.scan_result import ScanResult
from core.heuristics.url_analyzer.check.base64_detect.base64_segments import base64_segments
from core.heuristics.url_analyzer.check.parts_check import random_path_risk, query_no_value, query_contains_url, path_depth_risk, fragment_risk
from core.engine.registry.rule_registry import register

@register
class RandomPathRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="random_path_risk", category="url", severity="medium")

    def run(self, context):
        data = random_path_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class QueryNoValueRule(ScanRule):
    def __init__(self):
        super().__init__(name="query_no_value", category="url", severity="medium")

    def run(self, context):
        data = query_no_value(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class QueryContainsURLRule(ScanRule):
    def __init__(self):
        super().__init__(name="query_contains_url", category="url", severity="High")

    def run(self, context):
        data = query_contains_url(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class Base64SegmentRule(ScanRule):
    def __init__(self):
        super().__init__(name="base64_segment", category="url", severity="medium")

    def run(self, context):
        data = base64_segments(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class PathDepthRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="path_depth_risk", category="url", severity="medium")

    def run(self, context):
        data = path_depth_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class FragmentRiskRule(ScanRule):
    def __init__(self):
        super().__init__(name="fragment_risk", category="url", severity="medium")

    def run(self, context):
        data = fragment_risk(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)