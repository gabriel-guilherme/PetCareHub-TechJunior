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
    LLM_REASONING: bool = False
    PORT: int = Field(default=8001, ge=1, le=65535)

    # Regras exibidas pelo chatbot (RN06 e RF18).
    HORARIO_FUNCIONAMENTO: str = (
        "de segunda a sábado, das 8h às 18h, com horários a cada 30 minutos"
    )
    CANAL_ATENDIMENTO_HUMANO: str = "procure a recepção do PetCare Hub"
    TIMEZONE: str = "America/Sao_Paulo"

    # Limites de tempo (RNF11)
    BACKEND_TIMEOUT_SECONDS: float = Field(default=3.0, gt=0)
    LLM_TIMEOUT_SECONDS: float = Field(default=6.0, gt=0)

    # Limites do contrato de entrada do chat.
    CHAT_MAX_MENSAGEM: int = Field(default=1000, ge=1)
    CHAT_MAX_HISTORICO: int = Field(default=20, ge=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
