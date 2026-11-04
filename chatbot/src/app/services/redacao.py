import re
from typing import Protocol

from app.core.texto import normalizar

NUMEROS = re.compile(r"\d+")


class Redator(Protocol):
    async def redigir(self, mensagem: str, rascunho: str, timeout: float) -> str | None: ...


def redacao_confiavel(rascunho: str, redigido: str, preservar: tuple[str, ...]) -> bool:
    """Recusa o texto do modelo se ele trouxer um número que não está no
    rascunho ou perder um trecho obrigatório."""
    permitidos = {int(n) for n in NUMEROS.findall(rascunho)}
    if any(int(n) not in permitidos for n in NUMEROS.findall(redigido)):
        return False
    texto = normalizar(redigido)
    return all(normalizar(trecho) in texto for trecho in preservar)
