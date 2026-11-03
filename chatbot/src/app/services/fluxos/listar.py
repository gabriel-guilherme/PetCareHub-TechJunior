import asyncio
from datetime import datetime

from app.core.texto import formatar_data_hora
from app.prompts import mensagens
from app.schemas.backend import Agendamento, StatusAgendamento
from app.services.fluxos import Resultado
from app.services.intencao import Classificacao
from app.tools.backend import ClienteBackend, ErroBackend, NaoAutenticado

MAXIMO_ITENS = 5

STATUS_EXIBIDO = {
    StatusAgendamento.AGENDADO: "AGENDADO",
    StatusAgendamento.CANCELADO: "CANCELADO",
    StatusAgendamento.CONCLUIDO: "CONCLUÍDO",
}
STATUS_NA_FRASE = {
    StatusAgendamento.AGENDADO: "ativos",
    StatusAgendamento.CANCELADO: "cancelados",
    StatusAgendamento.CONCLUIDO: "concluídos",
}


async def listar_agendamentos(
    classificacao: Classificacao,
    backend: ClienteBackend,
    token: str,
    agora: datetime,
) -> Resultado:
    try:
        agendamentos, pets, servicos = await asyncio.gather(
            backend.listar_agendamentos(token, classificacao.status),
            backend.listar_pets(token),
            backend.listar_servicos(),
        )
    except NaoAutenticado:
        return Resultado(mensagens.SESSAO_EXPIRADA, login_necessario=True)
    except ErroBackend:
        return Resultado(mensagens.FALHA_BACKEND)

    if not agendamentos:
        if classificacao.status:
            status = STATUS_NA_FRASE[classificacao.status]
            return Resultado(mensagens.SEM_AGENDAMENTOS_STATUS.format(status=status))
        return Resultado(mensagens.SEM_AGENDAMENTOS)

    nomes_pets = {p.id: p.nome for p in pets}
    nomes_servicos = {s.id: s.nome for s in servicos}
    ordenados = ordenar(agendamentos, agora)

    linhas = [
        f"{i}. {nomes_pets.get(a.pet_id, 'Pet')} — "
        f"{nomes_servicos.get(a.servico_id, 'Serviço')} — "
        f"{formatar_data_hora(a.data_hora)} — {STATUS_EXIBIDO[a.status]}"
        for i, a in enumerate(ordenados[:MAXIMO_ITENS], start=1)
    ]
    restantes = len(ordenados) - MAXIMO_ITENS
    if restantes > 0:
        linhas.append(mensagens.LISTA_AGENDAMENTOS_RESTANTES.format(restantes=restantes))

    total = f"{len(ordenados)} agendamento" + ("s" if len(ordenados) > 1 else "")
    return Resultado(mensagens.LISTA_AGENDAMENTOS.format(total=total, itens="\n".join(linhas)))


def ordenar(agendamentos: list[Agendamento], agora: datetime) -> list[Agendamento]:
    """Primeiro os AGENDADO futuros, do mais próximo; depois os demais, do mais recente."""
    def proximo(a: Agendamento) -> bool:
        return a.status is StatusAgendamento.AGENDADO and a.data_hora >= agora

    futuros = sorted((a for a in agendamentos if proximo(a)), key=lambda a: a.data_hora)
    demais = sorted(
        (a for a in agendamentos if not proximo(a)), key=lambda a: a.data_hora, reverse=True
    )
    return futuros + demais
