from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from app.core.config import settings


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Intencao(str, Enum):
    FAQ = "FAQ"
    LISTAR_AGENDAMENTOS = "LISTAR_AGENDAMENTOS"
    CRIAR_AGENDAMENTO = "CRIAR_AGENDAMENTO"
    CANCELAR_AGENDAMENTO = "CANCELAR_AGENDAMENTO"
    FORA_DE_ESCOPO = "FORA_DE_ESCOPO"
    INDEFINIDA = "INDEFINIDA"


class MensagemHistorico(CamelModel):
    papel: Literal["tutor", "assistente"]
    texto: str = Field(max_length=settings.CHAT_MAX_MENSAGEM)


class ChatRequest(CamelModel):
    mensagem: str = Field(min_length=1, max_length=settings.CHAT_MAX_MENSAGEM)
    historico: list[MensagemHistorico] = Field(
        default_factory=list, max_length=settings.CHAT_MAX_HISTORICO
    )
    conversa_id: str | None = Field(default=None, max_length=64)

    @field_validator("mensagem")
    @classmethod
    def mensagem_nao_vazia(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("A mensagem não pode estar vazia.")
        return valor


class ChatResponse(CamelModel):
    resposta: str
    conversa_id: str
    intencao: Intencao
    login_necessario: bool = False
    aguardando_confirmacao: bool = False


class CampoErro(BaseModel):
    campo: str
    mensagem: str


class ErroResponse(BaseModel):
    status: int
    erro: str
    campos: list[CampoErro] = Field(default_factory=list)
