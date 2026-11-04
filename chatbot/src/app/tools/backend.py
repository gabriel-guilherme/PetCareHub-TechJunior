import logging
from datetime import date, time
from typing import Any

import httpx
from pydantic import ValidationError

from app.core.config import Settings, settings
from app.schemas.backend import (
    Agendamento,
    NovoAgendamento,
    Pet,
    Servico,
    StatusAgendamento,
    ler_horario,
)

logger = logging.getLogger(__name__)


class ErroBackend(Exception):
    """Base das falhas do backend. `mensagem` vem do campo `erro`, se houver."""

    def __init__(self, mensagem: str | None = None) -> None:
        super().__init__(mensagem or self.__class__.__name__)
        self.mensagem = mensagem


class BackendIndisponivel(ErroBackend):
    """Timeout, falha de conexão, erro 5xx ou resposta fora do contrato."""


class NaoAutenticado(ErroBackend):
    """401: token ausente, inválido ou expirado."""


class NaoEncontrado(ErroBackend):
    """403 ou 404: o recurso não existe ou não é do tutor (RN03)."""


class Conflito(ErroBackend):
    """409: horário já ocupado (RN07)."""


class RequisicaoInvalida(ErroBackend):
    """400 ou 422: regra de negócio violada (RN05, RN06, RN08...)."""


class ClienteBackend:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def fechar(self) -> None:
        await self._http.aclose()

    async def listar_servicos(self) -> list[Servico]:
        dados = await self._requisitar("GET", "/servicos")
        return self._ler_lista(Servico, dados)

    async def listar_pets(self, token: str) -> list[Pet]:
        dados = await self._requisitar("GET", "/pets", token=token)
        return self._ler_lista(Pet, dados)

    async def listar_horarios(self, servico_id: int, data: date, token: str) -> list[time]:
        dados = await self._requisitar(
            "GET",
            f"/servicos/{servico_id}/horarios",
            token=token,
            params={"data": data.isoformat()},
        )
        if not isinstance(dados, list):
            raise BackendIndisponivel("Lista de horários fora do contrato")
        try:
            return sorted(ler_horario(item) for item in dados)
        except ValueError as exc:
            raise BackendIndisponivel("Horário fora do contrato") from exc

    async def listar_agendamentos(
        self, token: str, status: StatusAgendamento | None = None
    ) -> list[Agendamento]:
        params = {"status": status.value} if status else None
        dados = await self._requisitar("GET", "/agendamentos", token=token, params=params)
        return self._ler_lista(Agendamento, dados)

    async def criar_agendamento(self, novo: NovoAgendamento, token: str) -> Agendamento:
        corpo = novo.model_dump(mode="json", by_alias=True, exclude_none=True)
        dados = await self._requisitar("POST", "/agendamentos", token=token, json=corpo)
        return self._ler(Agendamento, dados)

    async def cancelar_agendamento(self, agendamento_id: int, token: str) -> Agendamento:
        dados = await self._requisitar(
            "PATCH", f"/agendamentos/{agendamento_id}/cancelar", token=token
        )
        return self._ler(Agendamento, dados)

    async def _requisitar(
        self, metodo: str, caminho: str, token: str | None = None, **kwargs: Any
    ) -> Any:
        headers = {"Authorization": f"Bearer {token}"} if token else None
        try:
            resposta = await self._http.request(metodo, caminho, headers=headers, **kwargs)
        except httpx.TimeoutException as exc:
            logger.warning("Backend excedeu o tempo em %s %s", metodo, caminho)
            raise BackendIndisponivel() from exc
        except httpx.HTTPError as exc:
            logger.warning("Falha de conexão com o backend em %s %s: %s", metodo, caminho, exc)
            raise BackendIndisponivel() from exc

        if resposta.is_success:
            try:
                return resposta.json() if resposta.content else None
            except ValueError as exc:
                raise BackendIndisponivel("Resposta não é JSON") from exc
        raise self._erro_para(resposta)

    @staticmethod
    def _erro_para(resposta: httpx.Response) -> ErroBackend:
        try:
            corpo = resposta.json()
            mensagem = corpo.get("erro") if isinstance(corpo, dict) else None
        except ValueError:
            mensagem = None

        codigo = resposta.status_code
        if codigo == 401:
            return NaoAutenticado(mensagem)
        if codigo in (403, 404):
            return NaoEncontrado(mensagem)
        if codigo == 409:
            return Conflito(mensagem)
        if codigo in (400, 422):
            return RequisicaoInvalida(mensagem)
        logger.warning("Backend respondeu %s em %s", codigo, resposta.request.url)
        return BackendIndisponivel(mensagem)

    @staticmethod
    def _ler(modelo: type, dados: Any):
        try:
            return modelo.model_validate(dados)
        except ValidationError as exc:
            raise BackendIndisponivel(f"{modelo.__name__} fora do contrato") from exc

    @classmethod
    def _ler_lista(cls, modelo: type, dados: Any) -> list:
        if not isinstance(dados, list):
            raise BackendIndisponivel(f"Lista de {modelo.__name__} fora do contrato")
        return [cls._ler(modelo, item) for item in dados]


def criar_cliente_backend(
    config: Settings = settings, transport: httpx.AsyncBaseTransport | None = None
) -> ClienteBackend:
    """Cria o cliente. Com BACKEND_MOCK=true, usa a API simulada em memória."""
    if transport is None and config.BACKEND_MOCK:
        from app.tools.backend_mock import BackendSimulado

        transport = BackendSimulado(fuso=config.TIMEZONE).transporte()
    http = httpx.AsyncClient(
        base_url=config.BACKEND_API_URL.rstrip("/"),
        timeout=config.BACKEND_TIMEOUT_SECONDS,
        transport=transport,
    )
    return ClienteBackend(http)
