from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any
from core.models.http_result import HTTPResult

@dataclass(frozen=True)
class ScanContext:

    html: HTMLParser
    structure: dict[str, Any]
    response: HTTPResult