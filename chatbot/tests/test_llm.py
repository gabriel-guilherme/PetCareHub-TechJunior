import asyncio

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.schemas.chat import Intencao, MensagemHistorico
from app.services.llm import ClassificadorLLM, SaidaModelo
from conftest import config_teste


class EstruturadoFalso:
    def __init__(self, saida=None, atraso: float = 0, erro: Exception | None = None) -> None:
        self.saida, self.atraso, self.erro = saida, atraso, erro
        self.recebidas = None

    async def ainvoke(self, mensagens):
        self.recebidas = mensagens
        await asyncio.sleep(self.atraso)
        if self.erro:
            raise self.erro
        return self.saida


class ModeloFalso:
    def __init__(self, estruturado: EstruturadoFalso) -> None:
        self.estruturado = estruturado

    def with_structured_output(self, esquema):
        assert esquema is SaidaModelo
        return self.estruturado


def _classificador(estruturado: EstruturadoFalso, **config) -> ClassificadorLLM:
    return ClassificadorLLM(ModeloFalso(estruturado), config_teste(**config))


def test_converte_saida_do_modelo_em_classificacao() -> None:
    saida = SaidaModelo(intencao=Intencao.CRIAR_AGENDAMENTO, pet="Thor", servico="banho")

    resultado = asyncio.run(_classificador(EstruturadoFalso(saida)).classificar("oi", []))

    assert resultado.intencao is Intencao.CRIAR_AGENDAMENTO
    assert resultado.entidades.pet == "Thor"
    assert resultado.entidades.servico == "banho"


def test_monta_sistema_historico_recente_e_mensagem() -> None:
    estruturado = EstruturadoFalso(SaidaModelo(intencao=Intencao.FAQ))
    historico = [
        MensagemHistorico(papel="tutor" if i % 2 == 0 else "assistente", texto=f"m{i}")
        for i in range(6)
    ]

    asyncio.run(_classificador(estruturado).classificar("quanto custa?", historico))

    recebidas = estruturado.recebidas
    assert isinstance(recebidas[0], SystemMessage)
    assert [m.content for m in recebidas[1:-1]] == ["m2", "m3", "m4", "m5"]
    assert isinstance(recebidas[1], HumanMessage) and isinstance(recebidas[2], AIMessage)
    assert recebidas[-1].content == "quanto custa?"


def test_retorna_none_quando_modelo_estoura_timeout() -> None:
    classificador = _classificador(EstruturadoFalso(atraso=1), LLM_TIMEOUT_SECONDS=0.05)

    assert asyncio.run(classificador.classificar("oi", [])) is None


def test_retorna_none_quando_modelo_falha() -> None:
    classificador = _classificador(EstruturadoFalso(erro=ConnectionError("Ollama fora do ar")))

    assert asyncio.run(classificador.classificar("oi", [])) is None


def test_retorna_none_quando_saida_e_invalida() -> None:
    assert asyncio.run(_classificador(EstruturadoFalso(None)).classificar("oi", [])) is None
