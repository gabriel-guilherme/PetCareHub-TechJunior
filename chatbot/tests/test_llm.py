import asyncio

from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.config import Settings
from app.main import app
from app.prompts import mensagens
from app.schemas.chat import MensagemHistorico
from app.services.llm import GeradorLLM

client = TestClient(app)


class ModeloLento:
    async def ainvoke(self, _mensagens):
        await asyncio.sleep(1)


class ModeloComErro:
    async def ainvoke(self, _mensagens):
        raise ConnectionError("Ollama fora do ar")


def _config(**valores) -> Settings:
    return Settings(_env_file=None, **valores)


def test_gerador_devolve_texto_do_modelo() -> None:
    modelo = GenericFakeChatModel(messages=iter([AIMessage(content=" Olá, tutor! ")]))
    gerador = GeradorLLM(modelo, _config())

    assert asyncio.run(gerador.gerar("oi", [])) == "Olá, tutor!"


def test_gerador_monta_sistema_historico_e_mensagem_sem_token() -> None:
    gerador = GeradorLLM(GenericFakeChatModel(messages=iter([])), _config())
    historico = [
        MensagemHistorico(papel="tutor", texto="oi"),
        MensagemHistorico(papel="assistente", texto="Olá!"),
    ]

    montadas = gerador._montar_mensagens("quanto custa?", historico)

    assert [type(m) for m in montadas] == [SystemMessage, HumanMessage, AIMessage, HumanMessage]
    assert "procure a recepção do PetCare Hub" in montadas[0].content
    assert "segunda a sábado" in montadas[0].content
    assert montadas[-1].content == "quanto custa?"
    assert all("Bearer" not in m.content for m in montadas)


def test_gerador_retorna_none_quando_modelo_estoura_timeout() -> None:
    gerador = GeradorLLM(ModeloLento(), _config(LLM_TIMEOUT_SECONDS=0.05))

    assert asyncio.run(gerador.gerar("oi", [])) is None


def test_gerador_retorna_none_quando_modelo_falha() -> None:
    gerador = GeradorLLM(ModeloComErro(), _config())

    assert asyncio.run(gerador.gerar("oi", [])) is None


def test_chat_usa_resposta_do_modelo(gerador) -> None:
    response = client.post("/api/chat", json={"mensagem": "oi"})

    assert response.json()["resposta"] == "Resposta do modelo."
    assert gerador.chamadas[0][0] == "oi"


def test_chat_usa_mensagem_fixa_quando_modelo_falha(gerador) -> None:
    gerador.resposta = None

    response = client.post("/api/chat", json={"mensagem": "oi"})

    assert response.status_code == 200
    assert response.json()["resposta"] == mensagens.BOAS_VINDAS
