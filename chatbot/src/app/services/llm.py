import asyncio
import logging
from typing import Protocol

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from app.core.config import Settings, settings
from app.prompts.sistema import PROMPT_SISTEMA
from app.schemas.chat import MensagemHistorico

logger = logging.getLogger(__name__)


class GeradorResposta(Protocol):
    async def gerar(self, mensagem: str, historico: list[MensagemHistorico]) -> str | None: ...


def criar_modelo(config: Settings) -> BaseChatModel:
    return ChatOllama(
        model=config.LLM_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        temperature=0.2,
        reasoning=config.LLM_REASONING,
    )


class GeradorLLM:
    """Redige a resposta com o modelo local. Retorna None em erro ou timeout."""

    def __init__(self, modelo: BaseChatModel, config: Settings = settings) -> None:
        self._modelo = modelo
        self._config = config

    def _montar_mensagens(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> list[BaseMessage]:
        sistema = PROMPT_SISTEMA.format(
            horario_funcionamento=self._config.HORARIO_FUNCIONAMENTO,
            canal_atendimento_humano=self._config.CANAL_ATENDIMENTO_HUMANO,
        )
        mensagens: list[BaseMessage] = [SystemMessage(content=sistema)]
        for item in historico:
            classe = HumanMessage if item.papel == "tutor" else AIMessage
            mensagens.append(classe(content=item.texto))
        mensagens.append(HumanMessage(content=mensagem))
        return mensagens

    async def gerar(self, mensagem: str, historico: list[MensagemHistorico]) -> str | None:
        try:
            resposta = await asyncio.wait_for(
                self._modelo.ainvoke(self._montar_mensagens(mensagem, historico)),
                timeout=self._config.LLM_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            logger.warning("Modelo excedeu %ss", self._config.LLM_TIMEOUT_SECONDS)
            return None
        except Exception:
            logger.exception("Falha ao chamar o modelo")
            return None

        texto = resposta.content if isinstance(resposta.content, str) else ""
        return texto.strip() or None
