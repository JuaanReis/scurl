import asyncio
from functools import partial
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from time import perf_counter
from slowapi.util import get_remote_address
from ..schema.map_error import ErrorResponse
from core.engine.engine import run_engine
from scurl import config
from ..schema.map_result import (
    AnalyzeRequest,
    AnalyzeResponse,
    ScanResponse,
    TargetResponse
)

_rate_enabled = config.get("rate_limit", {}).get("enabled", False)
_rpm = config.get("rate_limit", {}).get("requests_per_minute", 10)
_limit_string = f"{_rpm}/minute" if _rate_enabled else "99999/minute"
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

MAX_CONCURRENT_SCANS = 20
_semaphore = asyncio.Semaphore(MAX_CONCURRENT_SCANS)

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"description": "URL inválida"},
        429: {"description": "Rate limit excedido"},
        503: {"description": "Servidor ocupado"},
    }
)
@limiter.limit(_limit_string)
async def analyze_url(request: Request, body: AnalyzeRequest):
    start = perf_counter()

    if _semaphore.locked():
        return JSONResponse(
                    status_code=503, 
                    content={
                        "error": "servidor ocupado, tente novamente"
                    }
                )

    scanner_config = config.get("scanner", {})
    async with _semaphore:
        loop = asyncio.get_running_loop()
        scan, target = await loop.run_in_executor(
            None, partial(
                run_engine, str(body.url), 
                    use_cache=body.use_cache, 
                    timeout=scanner_config.get("timeout", 5.0), 
                    processors=scanner_config.get("threads", 2), 
                    k=scanner_config.get("k", 5), 
                    retries=scanner_config.get("retries", 3)
                )
        )

    if "meta" in scan:
        scan["meta"]["scan_time_s"] = round(perf_counter() - start, 3) 

    if scan.get("status") == "error":
        return JSONResponse(status_code=400, content=scan)

    return AnalyzeResponse(scan=ScanResponse(**scan), target=TargetResponse(**target))