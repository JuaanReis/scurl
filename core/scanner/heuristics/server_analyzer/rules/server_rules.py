from ..check.domain_age import domain_age
from ..check.ssl_verify.ssl_verify import ssl_score
from ..check.dns_verify.dns_verify import dns_score
from ..check.rdap_field import rdap_metadata_incompleteness
from ..check.nameserver_diversity import nameserver_diversity
from core.models.scan_rule import ScanRule
from core.models.scan_result import ScanResult
from core.engine.rule_registry import register

@register
class SSLVerifyRule(ScanRule):
    def __init__(self):
        super().__init__(name="ssl_verify", category="server", severity="high")

    def run(self, context):
        data = ssl_score(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class DomainAgeRule(ScanRule):
    def __init__(self):
        super().__init__(name="domain_age", category="server", severity="medium")

    def run(self, context):
        data = domain_age(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class DNSVerifyRule(ScanRule):
    def __init__(self):
        super().__init__(name="dns_verify", category="server", severity="medium")

    def run(self, context):
        data = dns_score(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
@register
class RDAPFieldIncompletenessRule(ScanRule):
    def __init__(self):
        super().__init__(name="rdap_metadata", category="server", severity="medium")

    def run(self, context):
        data = rdap_metadata_incompleteness(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)

@register
class NameServerDiversityRule(ScanRule):
    def __init__(self):
        super().__init__(name="server_diversiry", category="server", severity="medium")

    def run(self, context):
        data = nameserver_diversity(context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
