from app.core.config import Settings


def test_settings_load_environment_values(monkeypatch) -> None:
    monkeypatch.setenv("BACKEND_API_URL", "http://localhost:8080/api")
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("PORT", "9001")

    settings = Settings(_env_file=None)

    assert settings.BACKEND_API_URL == "http://localhost:8080/api"
    assert settings.LLM_PROVIDER == "ollama"
    assert settings.LLM_API_KEY == "test-key"
    assert settings.LLM_MODEL == "test-model"
    assert settings.OLLAMA_BASE_URL == "http://localhost:11434"
    assert settings.PORT == 9001


def test_settings_have_cost_free_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.BACKEND_API_URL == "http://backend:8080/api"
    assert settings.LLM_PROVIDER == "ollama"
    assert settings.LLM_API_KEY is None
    assert settings.LLM_MODEL == "llama3.2"
    assert settings.OLLAMA_BASE_URL == "http://ollama:11434"
    assert settings.PORT == 8001
