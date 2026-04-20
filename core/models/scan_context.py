from dataclasses import dataclass, field
from time import time
from core.models.http_result import HTTPResult

@dataclass
class ScanContext:
    url: str
    start: float = field(default_factory=time)
    structure: dict = field(default_factory=dict)
    response: HTTPResult | None = None
    results: list = field(default_factory=list)
    results_map: dict[str, float | None] = field(default_factory=dict)
    scores: list[float] = field(default_factory=list)
    weights: list[float] = field(default_factory=list)
    heuristics: list[dict] = field(default_factory=list)
    score: float = 0.0
    classification: str = ""
    risk: str = ""