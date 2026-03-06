from dataclasses import dataclass
from uuid import uuid4

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent.agent import build_root_agent
from app.core.config import get_settings


@dataclass(slots=True)
class ChatResult:
    reply: str
    model_name: str
    session_id: str


class AgentService:
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=build_root_agent(),
            app_name=settings.app_name,
            session_service=self._session_service,
        )

    async def chat(self, message: str, user_id: str, session_id: str | None) -> ChatResult:
        if not self._settings.auth_configured:
            raise ValueError(
                "ADK credentials are not configured. Set GOOGLE_API_KEY or Vertex AI environment variables."
            )

        session_id = session_id or str(uuid4())
        await self._ensure_session(user_id=user_id, session_id=session_id)
        content = types.Content(role="user", parts=[types.Part(text=message)])

        final_response = None
        async for event in self._runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                final_response = self._extract_text(event)
                if final_response:
                    break

        if not final_response:
            raise ValueError("ADK agent did not produce a final response.")

        return ChatResult(
            reply=final_response,
            model_name=self._settings.model_name,
            session_id=session_id,
        )

    async def _ensure_session(self, user_id: str, session_id: str) -> None:
        session = await self._session_service.get_session(
            app_name=self._settings.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        if session is None:
            await self._session_service.create_session(
                app_name=self._settings.app_name,
                user_id=user_id,
                session_id=session_id,
            )

    @staticmethod
    def _extract_text(event: object) -> str | None:
        content = getattr(event, "content", None)
        if content is None:
            return None

        parts = getattr(content, "parts", None) or []
        chunks: list[str] = []
        for part in parts:
            text = getattr(part, "text", None)
            if text:
                chunks.append(text)

        return "\n".join(chunks).strip() or None


agent_service = AgentService()
