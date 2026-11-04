import asyncio
from datetime import date, datetime, time, timedelta

import httpx
import pytest

from app.schemas.backend import NovoAgendamento, StatusAgendamento
from app.tools.backend import (
    BackendIndisponivel,
    ClienteBackend,
    Conflito,
    NaoAutenticado,
    NaoEncontrado,
    RequisicaoInvalida,
    criar_cliente_backend,
)
from app.tools.backend_mock import BackendSimulado
from conftest import AGORA, TOKEN, config_teste as _config

SABADO = date(2026, 11, 7)


@pytest.fixture
def cliente(simulado: BackendSimulado) -> ClienteBackend:
    return criar_cliente_backend(_config(), transport=simulado.transporte())


def _rodar(coro):
    return asyncio.run(coro)


def _cliente_respondendo(status: int, json=None, content: bytes | None = None) -> ClienteBackend:
    def handler(_: httpx.Request) -> httpx.Response:
        if content is not None:
            return httpx.Response(status, content=content)
        return httpx.Response(status, json=json)

    return criar_cliente_backend(_config(), transport=httpx.MockTransport(handler))


def test_lista_servicos_sem_token(cliente, simulado) -> None:
    servicos = _rodar(cliente.listar_servicos())

    assert [s.nome for s in servicos][:2] == ["Banho", "Tosa"]
    assert servicos[1].preco == 60.0 and servicos[1].duracao_minutos == 60
    assert simulado.chamadas[0].caminho == "/servicos"
    assert simulado.chamadas[0].token is None


def test_token_vai_apenas_no_cabecalho(cliente, simulado) -> None:
    _rodar(cliente.listar_pets(TOKEN))

    chamada = simulado.chamadas[0]
    assert chamada.token == TOKEN
    assert chamada.corpo is None


def test_lista_apenas_pets_do_tutor(cliente) -> None:
    pets = _rodar(cliente.listar_pets(TOKEN))

    assert {p.nome for p in pets} == {"Thor", "Mia"}


def test_token_invalido_vira_nao_autenticado(cliente) -> None:
    with pytest.raises(NaoAutenticado):
        _rodar(cliente.listar_pets("token-falso"))


def test_horarios_livres_excluem_ocupados(cliente) -> None:
    _rodar(cliente.criar_agendamento(
        NovoAgendamento(pet_id=1, servico_id=1, data_hora=datetime.combine(SABADO, time(9, 0))),
        TOKEN,
    ))

    horarios = _rodar(cliente.listar_horarios(1, SABADO, TOKEN))

    assert horarios[0] == time(8, 0)
    assert time(9, 0) not in horarios
    assert horarios[-1] == time(17, 30)


def test_domingo_nao_tem_horarios(cliente) -> None:
    assert _rodar(cliente.listar_horarios(1, SABADO + timedelta(days=1), TOKEN)) == []


def test_horarios_aceitam_data_hora_completa() -> None:
    cliente = _cliente_respondendo(200, json=["2026-11-07T09:30:00", "08:00"])

    assert _rodar(cliente.listar_horarios(1, SABADO, TOKEN)) == [time(8, 0), time(9, 30)]


def test_lista_agendamentos_com_filtro_de_status(cliente, simulado) -> None:
    agendamentos = _rodar(cliente.listar_agendamentos(TOKEN, StatusAgendamento.CONCLUIDO))

    assert [a.status for a in agendamentos] == [StatusAgendamento.CONCLUIDO]
    assert simulado.chamadas[0].caminho == "/agendamentos"


def test_status_com_acento_e_aceito() -> None:
    item = {"id": 1, "petId": 1, "servicoId": 1,
            "dataHora": "2026-11-07T09:00:00", "status": "CONCLUÍDO"}
    cliente = _cliente_respondendo(200, json=[item])

    assert _rodar(cliente.listar_agendamentos(TOKEN))[0].status is StatusAgendamento.CONCLUIDO


def test_cria_agendamento_com_corpo_do_contrato(cliente, simulado) -> None:
    novo = NovoAgendamento(pet_id=1, servico_id=2, data_hora=datetime.combine(SABADO, time(9, 30)))

    criado = _rodar(cliente.criar_agendamento(novo, TOKEN))

    assert simulado.chamadas[0].corpo == {
        "petId": 1, "servicoId": 2, "dataHora": "2026-11-07T09:30:00",
    }
    assert criado.status is StatusAgendamento.AGENDADO
    assert criado.data_hora == datetime.combine(SABADO, time(9, 30))


def test_horario_ocupado_vira_conflito(cliente) -> None:
    novo = NovoAgendamento(pet_id=1, servico_id=2, data_hora=datetime.combine(SABADO, time(9, 30)))
    _rodar(cliente.criar_agendamento(novo, TOKEN))

    with pytest.raises(Conflito) as erro:
        _rodar(cliente.criar_agendamento(novo.model_copy(update={"pet_id": 2}), TOKEN))
    assert erro.value.mensagem == "Horário indisponível"


@pytest.mark.parametrize(
    ("data_hora", "mensagem"),
    [
        (AGORA - timedelta(hours=1), "O agendamento deve ser no futuro"),
        (datetime(2026, 11, 8, 10, 0), "Fora do horário de atendimento"),
        (datetime.combine(SABADO, time(9, 15)), "Fora do horário de atendimento"),
    ],
)
def test_regras_de_data_viram_requisicao_invalida(cliente, data_hora, mensagem) -> None:
    novo = NovoAgendamento(pet_id=1, servico_id=1, data_hora=data_hora)

    with pytest.raises(RequisicaoInvalida) as erro:
        _rodar(cliente.criar_agendamento(novo, TOKEN))
    assert erro.value.mensagem == mensagem


def test_pet_de_outro_tutor_vira_nao_encontrado(cliente) -> None:
    novo = NovoAgendamento(pet_id=3, servico_id=1, data_hora=datetime.combine(SABADO, time(9, 0)))

    with pytest.raises(NaoEncontrado):
        _rodar(cliente.criar_agendamento(novo, TOKEN))


def test_cancela_agendamento(cliente, simulado) -> None:
    cancelado = _rodar(cliente.cancelar_agendamento(1, TOKEN))

    assert cancelado.status is StatusAgendamento.CANCELADO
    assert simulado.chamadas[0].metodo == "PATCH"


def test_cancelamento_com_menos_de_2_horas_e_recusado(simulado, cliente) -> None:
    simulado.agendamentos[0]["dataHora"] = AGORA + timedelta(hours=1)

    with pytest.raises(RequisicaoInvalida):
        _rodar(cliente.cancelar_agendamento(1, TOKEN))


def test_cancelar_agendamento_de_outro_tutor_vira_nao_encontrado(cliente) -> None:
    with pytest.raises(NaoEncontrado):
        _rodar(cliente.cancelar_agendamento(3, TOKEN))


def test_erro_5xx_vira_backend_indisponivel(simulado, cliente) -> None:
    simulado.falhar_com = 500

    with pytest.raises(BackendIndisponivel):
        _rodar(cliente.listar_servicos())


def test_timeout_vira_backend_indisponivel() -> None:
    def handler(requisicao: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("lento", request=requisicao)

    cliente = criar_cliente_backend(_config(), transport=httpx.MockTransport(handler))

    with pytest.raises(BackendIndisponivel):
        _rodar(cliente.listar_servicos())


def test_backend_fora_do_ar_vira_backend_indisponivel() -> None:
    cliente = criar_cliente_backend(_config(BACKEND_TIMEOUT_SECONDS=0.2))
    cliente._http.base_url = "http://127.0.0.1:1/api"

    with pytest.raises(BackendIndisponivel):
        _rodar(cliente.listar_servicos())


@pytest.mark.parametrize(
    "resposta",
    [{"json": {"servicos": []}}, {"json": [{"nome": "sem id"}]}, {"content": b"<html>"}],
)
def test_resposta_fora_do_contrato_vira_backend_indisponivel(resposta) -> None:
    cliente = _cliente_respondendo(200, **resposta)

    with pytest.raises(BackendIndisponivel):
        _rodar(cliente.listar_servicos())


def test_flag_mock_usa_api_simulada() -> None:
    cliente = criar_cliente_backend(_config(BACKEND_MOCK=True))

    assert _rodar(cliente.listar_servicos())
