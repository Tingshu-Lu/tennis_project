from contextvars import ContextVar
from uuid import uuid4

_request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(request_id: str | None = None) -> str:
    value = request_id or str(uuid4())
    _request_id_var.set(value)
    return value


def get_request_id() -> str:
    return _request_id_var.get()
