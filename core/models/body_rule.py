from dataclasses import dataclass
from html.parser import HTMLParser
from core.models.http_result import HTTPResult
from core.models.scan_result import ScanResult

@dataclass
class BodyRule:

    html: HTMLParser
    structure: dict
    response: HTTPResult
    
    def run(self, context: dict) -> ScanResult:
        raise NotImplementedError