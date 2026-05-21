from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from os import getenv
from dotenv import load_dotenv
from app.api.router.analyze import router, limiter
from app.api.router.scans import router as scans_router
from fastapi.middleware.cors import CORSMiddleware
from providers.database.connection import init_db
from importlib.metadata import version
import uvicorn
from scurl import config
__version__ = version("scurl")
load_dotenv()
print(f"[DEBUG] SCURL_ENV={getenv('SCURL_ENV')}")
_docs_url = "/docs" if getenv("SCURL_ENV") != "production" else None
app = FastAPI(title="scurl", version=__version__, docs_url=_docs_url, redoc_url=None)

if config["server"]["cors"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.include_router(router)
app.include_router(scans_router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": "internal server error"})

@app.on_event("startup")
async def startup():
    try:
        init_db()
    except Exception as e:
        print(f"WARN DB init failed: {e}.")

@app.get("/health")
async def health():
    db_status = "ok"
    try:
        from providers.database.connection import get_connection
        get_connection().execute("SELECT 1")
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "version": __version__,
        "datetime": datetime.now(timezone.utc),
        "db": db_status,
    }

def run():
    uvicorn.run(
        "app.api.server:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        workers=config["server"]["workers"],
        reload=False
    )

if __name__ == "__main__":
    run()