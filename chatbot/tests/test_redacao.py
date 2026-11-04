import asyncio

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.main import app
from app.prompts import mensagens
from app.schemas.chat import ChatRequest, Intencao
from app.services.chat_service import ChatService
from app.services.intencao import Classificacao, Roteador
from app.services.llm import RedatorLLM
from app.services.redacao import redacao_confiavel
from app.tools.backend import criar_cliente_backend
from conftest import AGORA, TOKEN, ClassificadorFalso, RedatorFalso, config_teste

client = TestClient(app)


def _conversar(mensagem: str, token: str | None = None) -> str:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.post("/api/chat", json={"mensagem": mensagem}, headers=headers).json()["resposta"]


@pytest.mark.parametrize(
    ("redigido", "preservar", "confiavel"),
    [
        ("A tosa sai por R$ 60,00 e leva uns 60 minutos.", ("Tosa",), True),
        ("A tosa sai por R$ 55,00.", ("Tosa",), False),
        ("A tosa leva uns 90 minutos.", ("Tosa",), False),
        ("Custa R$ 60,00.", ("Tosa",), False),
        ("A TOSA custa 60 reais.", ("Tosa",), True),
    ],
)
def test_conferencia_da_redacao(redigido, preservar, confiavel) -> None:
    rascunho = "Tosa custa R$ 60,00 e dura cerca de 60 minutos."

    assert redacao_confiavel(rascunho, redigido, preservar) is confiavel


def test_resposta_usa_texto_do_modelo(redator: RedatorFalso) -> None:
    redator.texto = "Claro! A tosa custa R$ 60,00 e leva uns 60 minutos. Quer agendar?"

    assert _conversar("Quanto custa a tosa?") == redator.texto
    mensagem, rascunho, _ = redator.chamadas[0]
    assert mensagem == "Quanto custa a tosa?"
    assert rascunho.startswith("Tosa custa R$ 60,00")


def test_redacao_com_preco_inventado_volta_ao_rascunho(redator: RedatorFalso) -> None:
    redator.texto = "A tosa está em promoção por R$ 45,00!"

    assert _conversar("Quanto custa a tosa?").startswith("Tosa custa R$ 60,00")


@pytest.mark.parametrize(
    ("intencao", "mensagem", "token"),
    [
        (Intencao.FORA_DE_ESCOPO, "Me passa uma receita de bolo?", None),
        (Intencao.INDEFINIDA, "vocês fazem hidratação?", None),
        (Intencao.LISTAR_AGENDAMENTOS, "meus agendamentos", None),
        (Intencao.LISTAR_AGENDAMENTOS, "meus agendamentos", TOKEN),
        (Intencao.FAQ, "quais serviços vocês têm?", None),
    ],
)
def test_mensagens_fixas_nao_passam_pelo_modelo(
    classificador, redator, intencao, mensagem, token
) -> None:
    classificador.resultado = Classificacao(intencao=intencao)
    redator.texto = "Sim, realizamos hidratação!"

    assert _conversar(mensagem, token) != redator.texto
    assert redator.chamadas == []


def test_modelo_fora_do_ar_usa_rascunho(redator: RedatorFalso) -> None:
    assert _conversar("Quanto custa a tosa?").startswith("Tosa custa R$ 60,00")
    assert len(redator.chamadas) == 1


class Cronometro:
    def __init__(self, *marcas: float) -> None:
        self.marcas = list(marcas)

    def __call__(self) -> float:
        return self.marcas.pop(0) if len(self.marcas) > 1 else self.marcas[0]


def _servico(cronometro: Cronometro, redator: RedatorFalso, **config) -> ChatService:
    configuracao = config_teste(**config)
    return ChatService(
        Roteador(ClassificadorFalso()),
        criar_cliente_backend(configuracao),
        redator,
        config=configuracao,
        relogio=lambda: AGORA,
        cronometro=cronometro,
    )


FUNCIONAMENTO = mensagens.FUNCIONAMENTO.format(
    horario="de segunda a sábado, das 8h às 18h, com horários a cada 30 minutos"
)


def _responder(servico: ChatService, mensagem: str = "Vocês abrem domingo?") -> str:
    return asyncio.run(servico.responder(ChatRequest(mensagem=mensagem), None)).resposta


def test_timeout_da_redacao_respeita_o_prazo_total() -> None:
    redator = RedatorFalso()
    redator.texto = "Olá!"

    _responder(_servico(Cronometro(0.0, 6.5), redator))

    assert redator.chamadas[0][2] == pytest.approx(3.0)


def test_sem_tempo_restante_nao_chama_o_modelo() -> None:
    redator = RedatorFalso()
    redator.texto = "Olá!"

    resposta = _responder(_servico(Cronometro(0.0, 9.0), redator))

    assert resposta == FUNCIONAMENTO
    assert redator.chamadas == []


def test_redacao_desligada_nao_chama_o_modelo() -> None:
    redator = RedatorFalso()
    redator.texto = "Olá!"

    resposta = _responder(_servico(Cronometro(0.0), redator, LLM_REDACAO=False))

    assert resposta == FUNCIONAMENTO
    assert redator.chamadas == []


class ModeloLento:
    async def ainvoke(self, _mensagens):
        await asyncio.sleep(1)


def test_redator_llm_monta_prompt_com_mensagem_e_rascunho() -> None:
    redator = RedatorLLM(GenericFakeChatModel(messages=iter([])))

    montadas = redator._montar_mensagens("quanto custa?", "Tosa custa R$ 60,00.")

    assert [type(m) for m in montadas] == [SystemMessage, HumanMessage]
    assert "quanto custa?" in montadas[1].content
    assert "Tosa custa R$ 60,00." in montadas[1].content


def test_redator_llm_devolve_texto_do_modelo() -> None:
    modelo = GenericFakeChatModel(messages=iter([AIMessage(content=" Olá, tutor! ")]))

    assert asyncio.run(RedatorLLM(modelo).redigir("oi", "Olá!", 1)) == "Olá, tutor!"


def test_redator_llm_retorna_none_no_timeout() -> None:
    assert asyncio.run(RedatorLLM(ModeloLento()).redigir("oi", "Olá!", 0.05)) is None
