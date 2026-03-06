from google.adk.agents import Agent

from app.core.config import get_settings


def build_root_agent() -> Agent:
    settings = get_settings()
    return Agent(
        name="system_lives_agent",
        model=settings.model_name,
        description="A concise conversational assistant for the tennis_project service.",
        instruction=(
            "You are the tennis_project system agent. "
            "Respond clearly and briefly. "
            "If the user asks for search or external data, explain that search tools "
            "will be added in a later phase."
        ),
    )
