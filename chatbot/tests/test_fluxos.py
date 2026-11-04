from fastapi.testclient import TestClient

from app.main import app
from app.prompts import mensagens
from app.schemas.chat import Intencao
from app.services.intencao import Classificacao, Entidades
from conftest import AGORA, TOKEN

client = TestClient(app)


def _conversar(mensagem: str, token: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = client.post("/api/chat", json={"mensagem": mensagem}, headers=headers)
    assert response.status_code == 200
    return response.json()


def test_faq_preco_e_duracao_vem_do_catalogo() -> None:
    corpo = _conversar("Quanto custa a tosa?")

    assert corpo["intencao"] == "FAQ"
    assert corpo["resposta"].startswith("Tosa custa R$ 60,00 e dura cerca de 60 minutos.")
    assert mensagens.OFERTA_AGENDAR in corpo["resposta"]


def test_faq_encontra_servico_pelo_radical() -> None:
    assert "Vacinação custa R$ 80,00" in _conversar("qual o valor da vacina?")["resposta"]


def test_faq_sem_servico_citado_lista_o_catalogo() -> None:
    resposta = _conversar("Quais serviços vocês têm?")["resposta"]

    assert resposta.startswith("Estes são os nossos serviços:")
    assert "- Banho custa R$ 50,00" in resposta
    assert "- Consulta veterinária custa R$ 120,00" in resposta


def test_faq_servico_fora_do_catalogo(classificador) -> None:
    classificador.resultado = Classificacao(
        intencao=Intencao.FAQ, entidades=Entidades(servico="hidratação")
    )

    resposta = _conversar("Quanto custa a hidratação?")["resposta"]

    assert resposta.startswith("Não encontrei o serviço hidratação.")
    assert "Banho, Tosa, Consulta veterinária, Vacinação" in resposta


def test_faq_funcionamento_vem_da_configuracao(simulado) -> None:
    resposta = _conversar("Vocês abrem domingo?")["resposta"]

    assert resposta == "O atendimento é de segunda a sábado, das 8h às 18h, com horários a cada 30 minutos."
    assert simulado.chamadas == []


def test_faq_horarios_livres_oferece_agendamento() -> None:
    assert _conversar("Tem horário livre sábado?")["resposta"] == mensagens.HORARIOS_LIVRES


def test_faq_com_catalogo_fora_do_ar_nao_cita_preco(simulado) -> None:
    simulado.falhar_com = 500

    resposta = _conversar("Quanto custa a tosa?")["resposta"]

    assert resposta == mensagens.FALHA_BACKEND
    assert "R$" not in resposta


def test_fora_de_escopo_indica_canal_humano(classificador) -> None:
    classificador.resultado = Classificacao(intencao=Intencao.FORA_DE_ESCOPO)

    corpo = _conversar("Me passa uma receita de bolo?")

    assert corpo["intencao"] == "FORA_DE_ESCOPO"
    assert corpo["resposta"].endswith("procure a recepção do PetCare Hub.")


def test_mensagem_sem_pedido_recebe_boas_vindas() -> None:
    corpo = _conversar("oi")

    assert corpo["intencao"] == "INDEFINIDA"
    assert corpo["resposta"] == mensagens.BOAS_VINDAS


def test_listar_sem_token_pede_login_sem_chamar_backend(simulado) -> None:
    corpo = _conversar("Quais são meus agendamentos?")

    assert corpo["loginNecessario"] is True
    assert corpo["resposta"] == mensagens.LOGIN_NECESSARIO
    assert simulado.chamadas == []


def test_listar_mostra_futuros_primeiro_com_nomes() -> None:
    corpo = _conversar("Quais são meus agendamentos?", TOKEN)

    assert corpo["intencao"] == "LISTAR_AGENDAMENTOS"
    assert corpo["resposta"] == (
        "Encontrei 2 agendamentos:\n"
        "1. Thor — Banho — quarta, 04/11, às 09h30 — AGENDADO\n"
        "2. Mia — Vacinação — sexta, 23/10, às 10h00 — CONCLUÍDO"
    )


def test_listar_filtra_por_status(simulado) -> None:
    corpo = _conversar("Meus agendamentos concluídos", TOKEN)

    assert corpo["resposta"].startswith("Encontrei 1 agendamento:\n1. Mia")
    chamada = next(c for c in simulado.chamadas if c.caminho == "/agendamentos")
    assert chamada.token == TOKEN


def test_listar_sem_resultados_com_status() -> None:
    assert _conversar("Meus agendamentos cancelados", TOKEN)["resposta"] == (
        "Não encontrei agendamentos cancelados na sua conta."
    )


def test_listar_sem_agendamentos_oferece_agendar(simulado) -> None:
    simulado.agendamentos.clear()

    assert _conversar("Quais são meus agendamentos?", TOKEN)["resposta"] == (
        mensagens.SEM_AGENDAMENTOS
    )


def test_listar_limita_a_5_itens(simulado) -> None:
    base = simulado.agendamentos[0]
    for i in range(5):
        simulado.agendamentos.append({**base, "id": 10 + i, "dataHora": AGORA.replace(day=20 + i)})

    resposta = _conversar("Quais são meus agendamentos?", TOKEN)["resposta"]

    assert resposta.startswith("Encontrei 7 agendamentos:")
    assert "5. " in resposta and "6. " not in resposta
    assert resposta.endswith("e mais 2.")


def test_listar_com_token_expirado_pede_login() -> None:
    corpo = _conversar("Quais são meus agendamentos?", "token-expirado")

    assert corpo["loginNecessario"] is True
    assert corpo["resposta"] == mensagens.SESSAO_EXPIRADA


def test_listar_com_backend_fora_do_ar(simulado) -> None:
    simulado.falhar_com = 503

    corpo = _conversar("Quais são meus agendamentos?", TOKEN)

    assert corpo["resposta"] == mensagens.FALHA_BACKEND
    assert corpo["loginNecessario"] is False


def test_id_de_tutor_na_mensagem_nao_muda_a_chamada(simulado) -> None:
    resposta = _conversar("Meus agendamentos do tutor 2, email bob@x.com", TOKEN)["resposta"]

    assert "Bob" not in resposta
    assert all(c.token == TOKEN for c in simulado.chamadas if c.caminho != "/servicos")
