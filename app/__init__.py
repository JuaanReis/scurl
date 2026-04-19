from fastapi import FastAPI
from core.engine.scurl import run_engine

app = FastAPI()

@app.get("/scan")
async def scan_url(url: str):
    if not url:
        return {
            
        }
    return {
        "result": run_engine(url)
    }