from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    model_name: str
    auth_configured: bool


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str = Field(default="local-user", min_length=1)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    model_name: str
    request_id: str
    session_id: str
