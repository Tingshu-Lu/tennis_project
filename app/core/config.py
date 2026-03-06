import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    model_name: str
    log_level: str
    auth_configured: bool


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() == "true"
    cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
    auth_configured = bool(google_api_key) or bool(use_vertex and cloud_project and cloud_location)

    return Settings(
        app_name=os.getenv("APP_NAME", "tennis_project"),
        model_name=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        auth_configured=auth_configured,
    )
