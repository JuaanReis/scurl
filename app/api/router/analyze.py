from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from ..schema.map_result import AnalyzeRequest, AnalyzeResponse, ScanResponse, TargetResponse
from ..schema.map_error import ErrorResponse
from core.engine.engine import run_engine
import asyncio
from functools import partial

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    operation_id="analyze_url",
    responses={
        400: {"model": ErrorResponse},
        422: {"description": "URL inválida"},
        429: {"description": "Rate limit excedido"},
    }
)
@limiter.limit("10/minute")
async def analyze_url(request: Request, body: AnalyzeRequest):
    scan, target = await asyncio.get_running_loop().run_in_executor(
        None, partial(run_engine, str(body.url), use_cache=body.use_cache)
    )

    if scan.get("status") == "error":
        return JSONResponse(status_code=400, content=scan)

    return AnalyzeResponse(scan=ScanResponse(**scan), target=TargetResponse(**target))