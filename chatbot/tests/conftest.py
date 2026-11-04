from datetime import datetime

import pytest

from app.core.config import Settings
from app.main import app
from app.schemas.chat import MensagemHistorico
from app.services.chat_service import ChatService, get_chat_service
from app.services.intencao import Classificacao, Roteador
from app.tools.backend import criar_cliente_backend
from app.tools.backend_mock import BackendSimulado

# Segunda-feira, 10h, para os testes não dependerem do relógio.
AGORA = datetime(2026, 11, 2, 10, 0)
TOKEN = "token-tutor-1"


class ClassificadorFalso:
    """Sem resultado definido, simula o modelo fora do ar (usa palavras-chave)."""

    def __init__(self) -> None:
        self.resultado: Classificacao | None = None
        self.chamadas: list[tuple[str, list[MensagemHistorico]]] = []

    async def classificar(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> Classificacao | None:
        self.chamadas.append((mensagem, historico))
        return self.resultado


class RedatorFalso:
    """Sem texto definido, simula o modelo fora do ar (usa o rascunho)."""

    def __init__(self) -> None:
        self.texto: str | None = None
        self.chamadas: list[tuple[str, str, float]] = []

    async def redigir(self, mensagem: str, rascunho: str, timeout: float) -> str | None:
        self.chamadas.append((mensagem, rascunho, timeout))
        return self.texto


def config_teste(**valores) -> Settings:
    return Settings(_env_file=None, BACKEND_API_URL="http://backend/api", **valores)


@pytest.fixture
def classificador() -> ClassificadorFalso:
    return ClassificadorFalso()


@pytest.fixture
def redator() -> RedatorFalso:
    return RedatorFalso()


@pytest.fixture
def simulado() -> BackendSimulado:
    return BackendSimulado(agora=lambda: AGORA)


@pytest.fixture(autouse=True)
def servico_sem_dependencias(
    classificador: ClassificadorFalso, redator: RedatorFalso, simulado: BackendSimulado
):
    config = config_teste()
    servico = ChatService(
        Roteador(classificador),
        criar_cliente_backend(config, transport=simulado.transporte()),
        redator,
        config=config,
        relogio=lambda: AGORA,
    )
    app.dependency_overrides[get_chat_service] = lambda: servico
    yield
    app.dependency_overrides.clear()
