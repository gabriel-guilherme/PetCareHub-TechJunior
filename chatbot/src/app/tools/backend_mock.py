import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import httpx

TOKENS = {"token-tutor-1": 1, "token-tutor-2": 2}

ABERTURA = time(8, 0)
FECHAMENTO = time(18, 0)
INTERVALO_MINUTOS = 30
ANTECEDENCIA_CANCELAMENTO = timedelta(hours=2)


@dataclass
class Chamada:
    metodo: str
    caminho: str
    token: str | None
    corpo: dict | None


@dataclass
class BackendSimulado:
    fuso: str = "America/Sao_Paulo"
    agora: Callable[[], datetime] | None = None
    # Força uma resposta de erro.
    falhar_com: int | None = None
    chamadas: list[Chamada] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.servicos = [
            {"id": 1, "nome": "Banho", "descricao": "Banho com secagem",
             "duracaoMinutos": 30, "preco": 50.0},
            {"id": 2, "nome": "Tosa", "descricao": "Tosa higiênica ou completa",
             "duracaoMinutos": 60, "preco": 60.0},
            {"id": 3, "nome": "Consulta veterinária", "descricao": "Consulta clínica geral",
             "duracaoMinutos": 30, "preco": 120.0},
            {"id": 4, "nome": "Vacinação", "descricao": "Aplicação de vacinas",
             "duracaoMinutos": 30, "preco": 80.0},
        ]
        self.pets = [
            {"id": 1, "nome": "Thor", "especie": "CAO", "raca": "Labrador", "idade": 4, "tutorId": 1},
            {"id": 2, "nome": "Mia", "especie": "GATO", "raca": None, "idade": 2, "tutorId": 1},
            {"id": 3, "nome": "Bob", "especie": "CAO", "raca": None, "idade": 7, "tutorId": 2},
        ]
        proximo = self._proximo_dia_util(self._agora().date() + timedelta(days=2))
        self.agendamentos = [
            self._registro(1, 1, 1, datetime.combine(proximo, time(9, 30)), "AGENDADO"),
            self._registro(2, 2, 4, datetime.combine(
                self._agora().date() - timedelta(days=10), time(10, 0)), "CONCLUIDO"),
            self._registro(3, 3, 2, datetime.combine(proximo, time(14, 0)), "AGENDADO"),
        ]

    def transporte(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.tratar)

    # --- roteamento -------------------------------------------------------

    def tratar(self, requisicao: httpx.Request) -> httpx.Response:
        caminho = re.sub(r"^.*?/api", "", requisicao.url.path) or "/"
        token = self._token(requisicao)
        corpo = json.loads(requisicao.content) if requisicao.content else None
        self.chamadas.append(Chamada(requisicao.method, caminho, token, corpo))

        if self.falhar_com:
            return _erro(self.falhar_com, "Erro simulado")

        metodo = requisicao.method
        if metodo == "GET" and caminho == "/servicos":
            return httpx.Response(200, json=self.servicos)

        tutor_id = TOKENS.get(token or "")
        if tutor_id is None:
            return _erro(401, "Não autenticado")

        if metodo == "GET" and caminho == "/pets":
            return httpx.Response(200, json=[p for p in self.pets if p["tutorId"] == tutor_id])
        if metodo == "GET" and (m := re.fullmatch(r"/servicos/(\d+)/horarios", caminho)):
            return self._horarios(int(m[1]), requisicao.url.params.get("data"))
        if metodo == "GET" and caminho == "/agendamentos":
            return self._listar(tutor_id, requisicao.url.params.get("status"))
        if metodo == "POST" and caminho == "/agendamentos":
            return self._criar(tutor_id, corpo or {})
        if metodo == "PATCH" and (m := re.fullmatch(r"/agendamentos/(\d+)/cancelar", caminho)):
            return self._cancelar(tutor_id, int(m[1]))
        return _erro(404, "Recurso não encontrado")

    # --- endpoints --------------------------------------------------------

    def _horarios(self, servico_id: int, data_texto: str | None) -> httpx.Response:
        if not self._servico(servico_id):
            return _erro(404, "Serviço não encontrado")
        try:
            dia = date.fromisoformat(data_texto or "")
        except ValueError:
            return _erro(400, "Data inválida", [("data", "Use o formato AAAA-MM-DD")])

        livres = [
            inicio.strftime("%H:%M")
            for inicio in self._grade(dia)
            if inicio > self._agora() and not self._ocupado(servico_id, inicio)
        ]
        return httpx.Response(200, json=livres)

    def _listar(self, tutor_id: int, status: str | None) -> httpx.Response:
        itens = [a for a in self.agendamentos if self._dono(a) == tutor_id]
        if status:
            itens = [a for a in itens if a["status"] == status.upper()]
        return httpx.Response(200, json=[self._publico(a) for a in itens])

    def _criar(self, tutor_id: int, corpo: dict) -> httpx.Response:
        faltando = [c for c in ("petId", "servicoId", "dataHora") if corpo.get(c) is None]
        if faltando:
            return _erro(400, "Dados inválidos", [(c, "Campo obrigatório") for c in faltando])

        pet = self._pet(corpo["petId"])
        if not pet or pet["tutorId"] != tutor_id:
            return _erro(404, "Pet não encontrado")
        if not self._servico(corpo["servicoId"]):
            return _erro(404, "Serviço não encontrado")
        try:
            inicio = datetime.fromisoformat(corpo["dataHora"]).replace(tzinfo=None)
        except (TypeError, ValueError):
            return _erro(400, "Dados inválidos", [("dataHora", "Data e hora inválidas")])

        if inicio <= self._agora():
            return _erro(400, "O agendamento deve ser no futuro")
        if inicio not in self._grade(inicio.date()):
            return _erro(400, "Fora do horário de atendimento")
        if self._ocupado(corpo["servicoId"], inicio):
            return _erro(409, "Horário indisponível")

        novo = self._registro(
            max((a["id"] for a in self.agendamentos), default=0) + 1,
            corpo["petId"], corpo["servicoId"], inicio, "AGENDADO", corpo.get("observacao"),
        )
        self.agendamentos.append(novo)
        return httpx.Response(201, json=self._publico(novo))

    def _cancelar(self, tutor_id: int, agendamento_id: int) -> httpx.Response:
        agendamento = next((a for a in self.agendamentos if a["id"] == agendamento_id), None)
        if not agendamento or self._dono(agendamento) != tutor_id:
            return _erro(404, "Agendamento não encontrado")
        if agendamento["status"] != "AGENDADO":
            return _erro(400, "Só agendamentos com status AGENDADO podem ser cancelados")
        if agendamento["dataHora"] - self._agora() < ANTECEDENCIA_CANCELAMENTO:
            return _erro(400, "Cancelamento exige 2 horas de antecedência")

        agendamento["status"] = "CANCELADO"
        return httpx.Response(200, json=self._publico(agendamento))

    # --- apoio ------------------------------------------------------------

    def _agora(self) -> datetime:
        if self.agora:
            return self.agora()
        return datetime.now(ZoneInfo(self.fuso)).replace(tzinfo=None)

    @staticmethod
    def _proximo_dia_util(dia: date) -> date:
        return dia + timedelta(days=1) if dia.weekday() == 6 else dia

    @staticmethod
    def _grade(dia: date) -> list[datetime]:
        """Horários de início possíveis no dia (RN06)."""
        if dia.weekday() == 6:
            return []
        atual = datetime.combine(dia, ABERTURA)
        fim = datetime.combine(dia, FECHAMENTO)
        grade = []
        while atual < fim:
            grade.append(atual)
            atual += timedelta(minutes=INTERVALO_MINUTOS)
        return grade

    def _ocupado(self, servico_id: int, inicio: datetime) -> bool:
        return any(
            a["servicoId"] == servico_id and a["dataHora"] == inicio and a["status"] == "AGENDADO"
            for a in self.agendamentos
        )

    def _servico(self, servico_id: int) -> dict | None:
        return next((s for s in self.servicos if s["id"] == servico_id), None)

    def _pet(self, pet_id: int) -> dict | None:
        return next((p for p in self.pets if p["id"] == pet_id), None)

    def _dono(self, agendamento: dict) -> int | None:
        pet = self._pet(agendamento["petId"])
        return pet["tutorId"] if pet else None

    def _registro(
        self, id_: int, pet_id: int, servico_id: int, inicio: datetime,
        status: str, observacao: str | None = None,
    ) -> dict:
        return {
            "id": id_, "petId": pet_id, "servicoId": servico_id, "dataHora": inicio,
            "status": status, "observacao": observacao, "criadoEm": self._agora(),
        }

    @staticmethod
    def _publico(agendamento: dict) -> dict:
        return {
            **agendamento,
            "dataHora": agendamento["dataHora"].isoformat(timespec="seconds"),
            "criadoEm": agendamento["criadoEm"].isoformat(timespec="seconds"),
        }

    @staticmethod
    def _token(requisicao: httpx.Request) -> str | None:
        esquema, _, token = requisicao.headers.get("Authorization", "").partition(" ")
        return token.strip() or None if esquema.lower() == "bearer" else None


def _erro(status: int, erro: str, campos: list[tuple[str, str]] | None = None) -> httpx.Response:
    corpo = {
        "status": status,
        "erro": erro,
        "campos": [{"campo": c, "mensagem": m} for c, m in campos or []],
    }
    return httpx.Response(status, json=corpo)
