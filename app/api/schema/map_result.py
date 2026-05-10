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
    timestamp: str

class Result(BaseModel):
    score: float
    risk_level: str
    verdict: str

class Target(BaseModel):
    url: str
    scheme: str
    hostname: str
    registered_domain: str
    tld: str
    subdomains: list[str]
    subdomain_count: int
    netloc: str | None = None
    is_https: bool

class Network(BaseModel):
    status_code: int
    response_time_s: float

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

class AnalyzeResponse(BaseModel):
    status: str
    engine: EngineInfo
    meta: Meta
    result: Result
    target: Target
    network: Network
    stats: Stats
    heuristics: list[Heuristic]
    insight: list[str]

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