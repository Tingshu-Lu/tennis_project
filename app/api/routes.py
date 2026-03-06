from fastapi import APIRouter, HTTPException

from app.agent.service import agent_service
from app.api.schemas import ChatRequest, ChatResponse, HealthResponse
from app.core.config import get_settings
from app.core.request_context import get_request_id

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model_name=settings.model_name,
        auth_configured=settings.auth_configured,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    try:
        result = await agent_service.chat(
            message=payload.message,
            user_id=payload.user_id,
            session_id=payload.session_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(
        reply=result.reply,
        model_name=result.model_name,
        request_id=get_request_id(),
        session_id=result.session_id,
    )
