from core.models.scan_result import ScanResult
from core.models.body_rule import BodyRule
from core.models.scan_rule import ScanRule
from ..check.external_script import external_script
from ..check.favicon_check import favicon_check
from ..check.image_check import image_src_check
from ..check.redirect_check import redirect_check
from ..check.hidden_fields import hidden_fields_check
from ..check.password_input import password_input_check
from ..check.form_action import form_action_check
from ..check.response import parse_html_response

class ParseHtmlResponseRule():
    def run(self, context):
        tree, structure = parse_html_response(context)
        return BodyRule(response=tree, structure=structure) 
    
class ExternalScriptRule(ScanRule):
    def __init__(self):
        super().__init__(name="external_script", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = external_script(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class FaviconRule(ScanRule):
    def __init__(self):
        super().__init__(name="favicon_check", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = favicon_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class ImageSrcRule(ScanRule):
    def __init__(self):
        super().__init__(name="image_src_check", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = image_src_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class RedirectRule(ScanRule):
    def __init__(self):
        super().__init__(name="redirect_check", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = redirect_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class HiddenFieldsRule(ScanRule):
    def __init__(self):
        super().__init__(name="hidden_fields_check", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = hidden_fields_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class PasswordInputRule(ScanRule):
    def __init__(self):
        super().__init__(name="password_input_check", category="response", severity="medium")

    def run(self, context: BodyRule):
        data = password_input_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)
    
class FormActionRule(ScanRule):
    def __init__(self):
        super().__init__(name="form_action_check", category="response", severity="high")

    def run(self, context: BodyRule):
        data = form_action_check(context.get('html_parser'), context)
        return ScanResult(name=self.name, value=data.normalized, weight=data.weight, category=self.category, severity=self.severity, details=data.details)