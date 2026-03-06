from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.logging import RequestContextMiddleware, configure_logging

configure_logging()

app = FastAPI(title="tennis_project", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.include_router(api_router)
