from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    BACKEND_API_URL: str = "http://backend:8080/api"
    LLM_PROVIDER: str = "ollama"
    LLM_API_KEY: str | None = None
    LLM_MODEL: str = "llama3.2"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    PORT: int = Field(default=8001, ge=1, le=65535)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
