from dataclasses import dataclass
from core.models.scan_result import ScanResult
from .http_result import HTTPResult

@dataclass
class BodyRule:

    response: HTTPResult
    structure: dict
    
    def run(self, context: dict) -> ScanResult:
        raise NotImplementedError