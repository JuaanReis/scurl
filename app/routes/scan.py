from fastapi import APIRouter
from core.engine.scurl import run_engine

router = APIRouter()

@router.get("/scan")
async def scan_url(url: str):
    return {
        "result": run_engine(url)
    }