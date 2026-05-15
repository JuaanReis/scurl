from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api.router.analyze import router, limiter
from app.api.router.scans import router as scans_router
from providers.database.connection import init_db
from importlib.metadata import version
import uvicorn
__version__ = version("scurl")

app = FastAPI(title="scurl", version=__version__, docs_url="/docs", redoc_url=None)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.include_router(router)
app.include_router(scans_router)

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/health")
async def health():
    return {
        "status": "ok", "version": __version__
    }

def run():
    uvicorn.run("app.api.server:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    run()