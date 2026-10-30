from fastapi.testclient import TestClient

from app.api.chat import extrair_token
from app.main import app

client = TestClient(app)


def test_chat_retorna_contrato_com_conversa_id() -> None:
    response = client.post("/api/chat", json={"mensagem": "oi"})

    assert response.status_code == 200
    corpo = response.json()
    assert set(corpo) == {
        "resposta",
        "conversaId",
        "intencao",
        "loginNecessario",
        "aguardandoConfirmacao",
    }
    assert corpo["conversaId"]
    assert corpo["loginNecessario"] is False


def test_chat_mantem_conversa_id_enviado() -> None:
    response = client.post(
        "/api/chat",
        json={
            "mensagem": "oi",
            "conversaId": "abc123",
            "historico": [{"papel": "assistente", "texto": "Olá!"}],
        },
    )

    assert response.status_code == 200
    assert response.json()["conversaId"] == "abc123"


def test_chat_mensagem_vazia_retorna_400_no_formato_padrao() -> None:
    response = client.post("/api/chat", json={"mensagem": "   "})

    assert response.status_code == 400
    corpo = response.json()
    assert corpo["status"] == 400
    assert corpo["erro"] == "Dados inválidos"
    assert corpo["campos"][0]["campo"] == "mensagem"


def test_chat_mensagem_longa_demais_retorna_400() -> None:
    response = client.post("/api/chat", json={"mensagem": "a" * 1001})

    assert response.status_code == 400
    assert response.json()["campos"][0]["campo"] == "mensagem"


def test_chat_sem_corpo_retorna_400() -> None:
    response = client.post("/api/chat")

    assert response.status_code == 400
    assert response.json()["status"] == 400


def test_chat_papel_invalido_no_historico_retorna_400() -> None:
    response = client.post(
        "/api/chat",
        json={"mensagem": "oi", "historico": [{"papel": "sistema", "texto": "x"}]},
    )

    assert response.status_code == 400
    assert response.json()["campos"][0]["campo"].startswith("historico")


def test_extrair_token_aceita_apenas_bearer() -> None:
    assert extrair_token("Bearer abc.def") == "abc.def"
    assert extrair_token("bearer abc") == "abc"
    assert extrair_token("Basic abc") is None
    assert extrair_token("Bearer ") is None
    assert extrair_token(None) is None
