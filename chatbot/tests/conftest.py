import pytest

from app.main import app
from app.schemas.chat import MensagemHistorico
from app.services.chat_service import ChatService, get_chat_service


class GeradorFalso:
    def __init__(self, resposta: str | None = "Resposta do modelo.") -> None:
        self.resposta = resposta
        self.chamadas: list[tuple[str, list[MensagemHistorico]]] = []

    async def gerar(self, mensagem: str, historico: list[MensagemHistorico]) -> str | None:
        self.chamadas.append((mensagem, historico))
        return self.resposta


@pytest.fixture
def gerador() -> GeradorFalso:
    return GeradorFalso()


@pytest.fixture(autouse=True)
def servico_sem_ollama(gerador: GeradorFalso):
    app.dependency_overrides[get_chat_service] = lambda: ChatService(gerador)
    yield
    app.dependency_overrides.clear()
