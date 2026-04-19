from fastapi import FastAPI
from app.routes.scan import router as scan_router

app = FastAPI()

app.include_router(scan_router)