import re
from typing import Protocol

from pydantic import BaseModel, Field, field_validator

from app.core.texto import normalizar
from app.schemas.backend import StatusAgendamento
from app.schemas.chat import Intencao, MensagemHistorico


class Entidades(BaseModel):
    pet: str | None = Field(default=None, description="Nome do pet citado")
    servico: str | None = Field(default=None, description="Nome do serviço citado")
    data: str | None = Field(default=None, description="Data como o tutor escreveu")
    hora: str | None = Field(default=None, description="Hora como o tutor escreveu")

    @field_validator("pet", "servico", "data", "hora", mode="before")
    @classmethod
    def vazio_vira_none(cls, valor: object) -> object:
        if isinstance(valor, str):
            return valor.strip() or None
        return valor


class Classificacao(BaseModel):
    intencao: Intencao
    entidades: Entidades = Field(default_factory=Entidades)
    status: StatusAgendamento | None = None


class Classificador(Protocol):
    async def classificar(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> Classificacao | None: ...


PALAVRAS_CHAVE: list[tuple[Intencao, re.Pattern]] = [
    (Intencao.CANCELAR_AGENDAMENTO, re.compile(
        r"\b(cancelar|cancela|cancele|desmarcar|desmarca|desmarque)\b")),
    (Intencao.CRIAR_AGENDAMENTO, re.compile(
        r"\b(agendar|agende|marcar|marque|reservar|reserve)\b")),
    (Intencao.LISTAR_AGENDAMENTOS, re.compile(
        r"\b(meus|minhas) (agendamentos|horarios|consultas)\b|\btenho marcad|\bagendamentos\b")),
    (Intencao.FORA_DE_ESCOPO, re.compile(
        r"\b(remedio|remedios|medicamento|dose|sintoma|sintomas)\b|\bignore\b")),
    (Intencao.FAQ, re.compile(
        r"\b(preco|precos|quanto custa|valor|servico|servicos|horario|horarios|"
        r"abre|abrem|fecha|fecham|funciona|funcionamento|aberto|duracao|quanto tempo)\b")),
]

PALAVRAS_STATUS: list[tuple[StatusAgendamento, re.Pattern]] = [
    (StatusAgendamento.CANCELADO, re.compile(r"\bcancelad")),
    (StatusAgendamento.CONCLUIDO, re.compile(r"\b(concluid|realizad|finalizad)")),
    (StatusAgendamento.AGENDADO, re.compile(r"\b(ativos|ativas|proximos|proximas|futuros)\b")),
]


def classificar_por_palavras(mensagem: str) -> Classificacao:
    texto = normalizar(mensagem)
    intencao = next(
        (intencao for intencao, padrao in PALAVRAS_CHAVE if padrao.search(texto)),
        Intencao.INDEFINIDA,
    )
    return Classificacao(intencao=intencao)


def extrair_status(mensagem: str) -> StatusAgendamento | None:
    texto = normalizar(mensagem)
    return next((status for status, padrao in PALAVRAS_STATUS if padrao.search(texto)), None)


class Roteador:
    """Usa o modelo e cai nas palavras-chave quando ele falha ou não decide."""

    def __init__(self, classificador: Classificador) -> None:
        self._classificador = classificador

    async def classificar(
        self, mensagem: str, historico: list[MensagemHistorico]
    ) -> Classificacao:
        por_palavras = classificar_por_palavras(mensagem)
        pelo_modelo = await self._classificador.classificar(mensagem, historico)

        if pelo_modelo is None or pelo_modelo.intencao is Intencao.INDEFINIDA:
            resultado = por_palavras
        else:
            resultado = pelo_modelo
        return resultado.model_copy(update={"status": extrair_status(mensagem)})
