from uuid import uuid4

from app.core.config import settings
from app.prompts import mensagens
from app.schemas.chat import ChatRequest, ChatResponse, Intencao
from app.services.llm import GeradorLLM, GeradorResposta, criar_modelo


class ChatService:
    """Orquestra uma mensagem do tutor até a resposta do chatbot."""

    def __init__(self, gerador: GeradorResposta) -> None:
        self._gerador = gerador

    async def responder(self, requisicao: ChatRequest, token: str | None) -> ChatResponse:
        conversa_id = requisicao.conversa_id or uuid4().hex
        texto = await self._gerador.gerar(requisicao.mensagem, requisicao.historico)
        return ChatResponse(
            resposta=texto or mensagens.BOAS_VINDAS,
            conversa_id=conversa_id,
            intencao=Intencao.INDEFINIDA,
        )


chat_service = ChatService(GeradorLLM(criar_modelo(settings)))


def get_chat_service() -> ChatService:
    return chat_service
