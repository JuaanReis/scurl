from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import time
from urllib.parse import ParseResult
from core.models.http_result import HTTPResult

@dataclass
class ScanMeta:
    scan_id: str = ""
    url_hash: str = ""
    threads: int = 1
    start: float = field(default_factory=time)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

@dataclass
class ScanContext:
    url: str = ""
    parsed_url: ParseResult | None = None
    response: HTTPResult | None = None
    html: object | None = None    
    rdap: dict | None = None
    dns: dict | None = None
    ssl: dict | None = None
    results: list = field(default_factory=list)
    results_map: dict[str, float | None] = field(default_factory=dict)
    scores: list[float] = field(default_factory=list)
    weights: list[float] = field(default_factory=list)
    heuristics: list[dict] = field(default_factory=list)
    score: float = 0.0
    classification: str = ""
    risk: str = ""
    meta: ScanMeta = field(default_factory=ScanMeta)