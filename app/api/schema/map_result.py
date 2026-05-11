from pydantic import BaseModel, HttpUrl
from typing import Any

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class EngineInfo(BaseModel):
    name: str
    version: str

class Meta(BaseModel):
    scan_id: str
    scan_time_s: float
    url_hash: str
    threads: int
    timestamp: str

class Result(BaseModel):
    score: float
    risk_level: str
    verdict: str

class Stats(BaseModel):
    rules_total: int
    rules_triggered: int
    trigger_rate: float

class Heuristic(BaseModel):
    name: str
    category: str
    value: float
    weight: float
    contribution: float
    details: dict[str, Any]
    reasons: list[str]

class ScanResponse(BaseModel):
    status: str
    engine: EngineInfo
    meta: Meta
    result: Result
    stats: Stats
    heuristics: list[Heuristic]
    insight: list[str]

class Network(BaseModel):
    status_code: int | None
    response_time_s: float | None

class Raw(BaseModel):
    size_kb: float
    redirects: int
    headers: dict[str, str] | None = None
    chain: list[dict] | None = None

class TargetResponse(BaseModel):
    url: str
    scheme: str
    hostname: str
    registered_domain: str
    tld: str
    subdomains: list[str]
    subdomain_count: int
    is_https: bool
    network: Network
    raw: Raw

class AnalyzeResponse(BaseModel):
    scan: ScanResponse
    target: TargetResponse

class ScanSummary(BaseModel):
    url: str
    score: float
    risk_level: str
    verdict: str
    scan_id: str
    timestamp: str
    url_hash: str

class ScansListResponse(BaseModel):
    status: str
    total: int
    scans: list[ScanSummary]