"""DTOs da API do backend, conforme o contrato do documento de requisitos.

Campos extras enviados pelo backend são ignorados, para que mudanças pequenas
no DTO não quebrem o chatbot.
"""

from datetime import datetime, time
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from app.core.texto import sem_acentos


class DtoBackend(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="ignore"
    )


class StatusAgendamento(str, Enum):
    AGENDADO = "AGENDADO"
    CANCELADO = "CANCELADO"
    CONCLUIDO = "CONCLUIDO"


class Servico(DtoBackend):
    id: int
    nome: str
    descricao: str | None = None
    duracao_minutos: int | None = None
    preco: float | None = None


class Pet(DtoBackend):
    id: int
    nome: str
    especie: str | None = None
    raca: str | None = None
    idade: int | None = None


class Agendamento(DtoBackend):
    id: int
    pet_id: int
    servico_id: int
    data_hora: datetime
    status: StatusAgendamento
    observacao: str | None = None

    @field_validator("status", mode="before")
    @classmethod
    def aceitar_status_com_acento(cls, valor: object) -> object:
        return sem_acentos(valor).upper() if isinstance(valor, str) else valor


class NovoAgendamento(DtoBackend):
    pet_id: int
    servico_id: int
    data_hora: datetime
    observacao: str | None = None


def ler_horario(valor: object) -> time:
    """Aceita "09:30", "09:30:00" ou "2026-10-31T09:30:00"."""
    if isinstance(valor, dict):
        valor = valor.get("hora") or valor.get("dataHora") or valor.get("horario")
    if not isinstance(valor, str):
        raise ValueError(f"Horário em formato inesperado: {valor!r}")
    if "T" in valor:
        return datetime.fromisoformat(valor).time()
    return time.fromisoformat(valor)
