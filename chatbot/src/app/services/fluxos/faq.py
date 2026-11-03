import re

from app.core.config import Settings
from app.core.texto import formatar_preco, normalizar
from app.prompts import mensagens
from app.schemas.backend import Servico
from app.services.fluxos import Resultado
from app.services.intencao import Classificacao
from app.tools.backend import ClienteBackend, ErroBackend

FUNCIONAMENTO = re.compile(
    r"\b(abre|abrem|fecha|fecham|funciona|funcionam|funcionamento|aberto|aberta|"
    r"domingo|feriado|que horas)\b"
)
HORARIOS_LIVRES = re.compile(r"\b(livre|livres|disponivel|disponiveis|vaga|vagas)\b")
GENERICOS = {"servico", "servicos", "preco", "precos", "valor", "valores"}


async def responder_faq(
    mensagem: str,
    classificacao: Classificacao,
    backend: ClienteBackend,
    config: Settings,
) -> Resultado:
    texto = normalizar(mensagem)
    if HORARIOS_LIVRES.search(texto):
        return Resultado(mensagens.HORARIOS_LIVRES, redigir=True)
    if FUNCIONAMENTO.search(texto):
        horario = config.HORARIO_FUNCIONAMENTO
        return Resultado(mensagens.FUNCIONAMENTO.format(horario=horario), redigir=True)

    try:
        servicos = await backend.listar_servicos()
    except ErroBackend:
        return Resultado(mensagens.FALHA_BACKEND)

    citados = encontrar_servicos(texto, servicos)
    if citados:
        linhas = [descrever_servico(s) for s in citados]
        return Resultado(
            "\n".join([*linhas, mensagens.OFERTA_AGENDAR]),
            redigir=True,
            preservar=tuple(s.nome for s in citados),
        )

    servico_pedido = classificacao.entidades.servico
    if servico_pedido and normalizar(servico_pedido) not in GENERICOS and servicos:
        return Resultado(
            mensagens.SERVICO_NAO_ENCONTRADO.format(
                servico=servico_pedido, nomes=", ".join(s.nome for s in servicos),
            ),
            redigir=True,
            preservar=tuple(s.nome for s in servicos),
        )
    if not servicos:
        return Resultado(mensagens.FALHA_BACKEND)

    itens = "\n".join(f"- {descrever_servico(s)}" for s in servicos)
    return Resultado(mensagens.LISTA_SERVICOS.format(itens=itens))


def encontrar_servicos(texto_normalizado: str, servicos: list[Servico]) -> list[Servico]:
    """Serviços citados pelo nome completo ou pelo início da primeira palavra
    ("vacina" encontra "Vacinação")."""
    palavras = texto_normalizado.split()
    encontrados = []
    for servico in servicos:
        nome = normalizar(servico.nome)
        radical = nome.split()[0][:5] if nome else ""
        if nome in texto_normalizado or (
            len(radical) >= 4 and any(p.startswith(radical) for p in palavras)
        ):
            encontrados.append(servico)
    return encontrados


def descrever_servico(servico: Servico) -> str:
    partes = []
    if servico.preco is not None:
        partes.append(f"custa {formatar_preco(servico.preco)}")
    if servico.duracao_minutos:
        partes.append(f"dura cerca de {servico.duracao_minutos} minutos")
    if not partes:
        return f"{servico.nome}: não consegui confirmar preço e duração agora."
    return f"{servico.nome} {' e '.join(partes)}."
