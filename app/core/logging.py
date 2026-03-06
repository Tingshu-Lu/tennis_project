import json
import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.request_context import get_request_id, set_request_id


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level.upper())


def log_request(path: str, status_code: int, latency_ms: float) -> None:
    payload = {
        "path": path,
        "status_code": status_code,
        "latency_ms": round(latency_ms, 2),
        "request_id": get_request_id(),
    }
    logging.getLogger("app.request").info(json.dumps(payload, sort_keys=True))


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id")
        set_request_id(request_id)
        started_at = time.perf_counter()
        response = await call_next(request)
        response.headers["x-request-id"] = get_request_id()
        latency_ms = (time.perf_counter() - started_at) * 1000
        log_request(request.url.path, response.status_code, latency_ms)
        return response
