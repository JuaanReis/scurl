from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..schema.map_result import AnalyzeRequest, AnalyzeResponse
from ..schema.map_error import ErrorResponse
from core.engine.scurl import run_engine

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_url(request: AnalyzeRequest):
    result = run_engine(str(request.url))

    if result.get("status") == "error":
        return JSONResponse(
            status_code=400,
            content=result
        )

    return result