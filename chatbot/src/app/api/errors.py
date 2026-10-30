from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.chat import CampoErro, ErroResponse

MENSAGENS_HTTP = {
    400: "Requisição inválida",
    404: "Recurso não encontrado",
    405: "Método não permitido",
    500: "Erro interno do chatbot",
}


def _resposta_erro(status: int, erro: str, campos: list[CampoErro] | None = None) -> JSONResponse:
    corpo = ErroResponse(status=status, erro=erro, campos=campos or [])
    return JSONResponse(status_code=status, content=corpo.model_dump())


def _nome_campo(loc: tuple) -> str:
    partes = [str(parte) for parte in loc if parte != "body"]
    return ".".join(partes) or "body"


async def tratar_validacao(_: Request, exc: RequestValidationError) -> JSONResponse:
    campos = [
        CampoErro(campo=_nome_campo(erro["loc"]), mensagem=erro["msg"])
        for erro in exc.errors()
    ]
    return _resposta_erro(400, "Dados inválidos", campos)


async def tratar_http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    erro = MENSAGENS_HTTP.get(exc.status_code, "Erro na requisição")
    return _resposta_erro(exc.status_code, erro)


async def tratar_inesperado(_: Request, __: Exception) -> JSONResponse:
    return _resposta_erro(500, MENSAGENS_HTTP[500])


def registrar_tratadores(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, tratar_validacao)
    app.add_exception_handler(StarletteHTTPException, tratar_http)
    app.add_exception_handler(Exception, tratar_inesperado)
