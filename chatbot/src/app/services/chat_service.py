import logging
import time
from collections.abc import Callable
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.core.config import Settings, settings
from app.prompts import mensagens
from app.schemas.chat import ChatRequest, ChatResponse, Intencao
from app.services.fluxos import Resultado
from app.services.fluxos.faq import responder_faq
from app.services.fluxos.listar import listar_agendamentos
from app.services.intencao import Classificacao, Roteador
from app.services.llm import ClassificadorLLM, RedatorLLM, criar_modelo
from app.services.redacao import Redator, redacao_confiavel
from app.tools.backend import ClienteBackend, criar_cliente_backend

logger = logging.getLogger(__name__)

EXIGEM_LOGIN = {
    Intencao.LISTAR_AGENDAMENTOS,
    Intencao.CRIAR_AGENDAMENTO,
    Intencao.CANCELAR_AGENDAMENTO,
}
FOLGA_SECONDS = 0.5
TEMPO_MINIMO_REDACAO_SECONDS = 1.0


class ChatService:
    """Classifica a mensagem, executa o fluxo da intenção e redige a resposta."""

    def __init__(
        self,
        roteador: Roteador,
        backend: ClienteBackend,
        redator: Redator | None = None,
        config: Settings = settings,
        relogio: Callable[[], datetime] | None = None,
        cronometro: Callable[[], float] = time.monotonic,
    ) -> None:
        self._roteador = roteador
        self.backend = backend
        self._redator = redator
        self._config = config
        self._relogio = relogio or self._agora_local
        self._cronometro = cronometro

    async def responder(self, requisicao: ChatRequest, token: str | None) -> ChatResponse:
        inicio = self._cronometro()
        conversa_id = requisicao.conversa_id or uuid4().hex
        classificacao = await self._roteador.classificar(
            requisicao.mensagem, requisicao.historico
        )
        resultado = await self._executar_fluxo(requisicao.mensagem, classificacao, token)
        texto = await self._redigir(requisicao.mensagem, resultado, inicio)

        return ChatResponse(
            resposta=texto,
            conversa_id=conversa_id,
            intencao=classificacao.intencao,
            login_necessario=resultado.login_necessario,
            aguardando_confirmacao=resultado.aguardando_confirmacao,
        )

    async def _executar_fluxo(
        self, mensagem: str, classificacao: Classificacao, token: str | None
    ) -> Resultado:
        intencao = classificacao.intencao
        if intencao in EXIGEM_LOGIN and not token:
            return Resultado(mensagens.LOGIN_NECESSARIO, login_necessario=True)
        if intencao is Intencao.FAQ:
            return await responder_faq(mensagem, classificacao, self.backend, self._config)
        if intencao is Intencao.LISTAR_AGENDAMENTOS:
            return await listar_agendamentos(classificacao, self.backend, token, self._relogio())
        if intencao is Intencao.CRIAR_AGENDAMENTO:
            return Resultado(mensagens.AGENDAMENTO_EM_BREVE.format(acao="marcar"))
        if intencao is Intencao.CANCELAR_AGENDAMENTO:
            return Resultado(mensagens.AGENDAMENTO_EM_BREVE.format(acao="cancelar"))
        if intencao is Intencao.FORA_DE_ESCOPO:
            canal = self._config.CANAL_ATENDIMENTO_HUMANO
            return Resultado(mensagens.FORA_DE_ESCOPO.format(canal=canal))
        return Resultado(mensagens.BOAS_VINDAS)

    async def _redigir(self, mensagem: str, resultado: Resultado, inicio: float) -> str:
        """Usa o texto do modelo só se couber no prazo e passar na conferência;
        senão, devolve o rascunho do fluxo."""
        if not (resultado.redigir and self._redator and self._config.LLM_REDACAO):
            return resultado.texto

        restante = (
            self._config.TEMPO_MAXIMO_RESPOSTA_SECONDS
            - (self._cronometro() - inicio)
            - FOLGA_SECONDS
        )
        timeout = min(self._config.LLM_TIMEOUT_SECONDS, restante)
        if timeout < TEMPO_MINIMO_REDACAO_SECONDS:
            return resultado.texto

        redigido = await self._redator.redigir(mensagem, resultado.texto, timeout)
        if redigido is None:
            return resultado.texto
        if not redacao_confiavel(resultado.texto, redigido, resultado.preservar):
            logger.warning("Redação descartada por alterar dados do rascunho")
            return resultado.texto
        return redigido

    def _agora_local(self) -> datetime:
        return datetime.now(ZoneInfo(self._config.TIMEZONE)).replace(tzinfo=None)


chat_service = ChatService(
    Roteador(ClassificadorLLM(criar_modelo(settings))),
    criar_cliente_backend(settings),
    RedatorLLM(criar_modelo(settings, temperatura=0.3)),
)


def get_chat_service() -> ChatService:
    return chat_service
