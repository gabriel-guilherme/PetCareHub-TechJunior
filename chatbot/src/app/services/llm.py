import asyncio
import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from app.core.config import Settings, settings
from app.prompts.sistema import PROMPT_CLASSIFICACAO, PROMPT_REDACAO
from app.schemas.chat import Intencao, MensagemHistorico
from app.services.intencao import Classificacao, Entidades

logger = logging.getLogger(__name__)

HISTORICO_NO_PROMPT = 4


class SaidaModelo(Entidades):
    intencao: Intencao


def criar_modelo(config: Settings, temperatura: float = 0) -> BaseChatModel:
    return ChatOllama(
        model=config.LLM_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        temperature=temperatura,
        reasoning=config.LLM_REASONING,
    )


class ClassificadorLLM:
    """Classifica a intenção com o modelo local. Retorna None em erro ou timeout."""

    def __init__(self, modelo: BaseChatModel, config: Settings = settings) -> None:
        self._estruturado = modelo.with_structured_output(SaidaModelo)
        self._config = config

    def _montar_mensagens(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> list[BaseMessage]:
        mensagens: list[BaseMessage] = [SystemMessage(content=PROMPT_CLASSIFICACAO)]
        for item in historico[-HISTORICO_NO_PROMPT:]:
            classe = HumanMessage if item.papel == "tutor" else AIMessage
            mensagens.append(classe(content=item.texto))
        mensagens.append(HumanMessage(content=mensagem))
        return mensagens

    async def classificar(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> Classificacao | None:
        try:
            saida = await asyncio.wait_for(
                self._estruturado.ainvoke(self._montar_mensagens(mensagem, historico)),
                timeout=self._config.LLM_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            logger.warning("Modelo excedeu %ss", self._config.LLM_TIMEOUT_SECONDS)
            return None
        except Exception:
            logger.exception("Falha ao chamar o modelo")
            return None

        if not isinstance(saida, SaidaModelo):
            return None
        entidades = Entidades.model_validate(saida.model_dump(exclude={"intencao"}))
        return Classificacao(intencao=saida.intencao, entidades=entidades)


class RedatorLLM:
    """Reescreve o rascunho dos fluxos. Retorna None em erro ou timeout."""

    def __init__(self, modelo: BaseChatModel) -> None:
        self._modelo = modelo

    @staticmethod
    def _montar_mensagens(mensagem: str, rascunho: str) -> list[BaseMessage]:
        pedido = f"Mensagem do tutor:\n{mensagem}\n\nResposta base:\n{rascunho}"
        return [SystemMessage(content=PROMPT_REDACAO), HumanMessage(content=pedido)]

    async def redigir(self, mensagem: str, rascunho: str, timeout: float) -> str | None:
        try:
            resposta = await asyncio.wait_for(
                self._modelo.ainvoke(self._montar_mensagens(mensagem, rascunho)),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            logger.warning("Redação excedeu %.1fs", timeout)
            return None
        except Exception:
            logger.exception("Falha ao redigir com o modelo")
            return None

        texto = resposta.content if isinstance(resposta.content, str) else ""
        return texto.strip() or None
