from fastapi import FastAPI
from .router.analyze import router

app = FastAPI(title="scurl API")
app.include_router(router)