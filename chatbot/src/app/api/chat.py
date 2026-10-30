from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.schemas.chat import ChatRequest, ChatResponse, ErroResponse
from app.services.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/api")


def extrair_token(
    authorization: Annotated[str | None, Header()] = None,
) -> str | None:
    """Lê o JWT do cabeçalho. O token só é repassado ao backend, nunca ao modelo."""
    if not authorization:
        return None
    esquema, _, token = authorization.partition(" ")
    if esquema.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


@router.post(
    "/chat",
    tags=["chat"],
    response_model=ChatResponse,
    response_model_by_alias=True,
    responses={400: {"model": ErroResponse}},
)
async def conversar(
    requisicao: ChatRequest,
    token: Annotated[str | None, Depends(extrair_token)],
    servico: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    return await servico.responder(requisicao, token)
