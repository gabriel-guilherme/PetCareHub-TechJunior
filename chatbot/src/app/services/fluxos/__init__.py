from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    texto: str
    login_necessario: bool = False
    aguardando_confirmacao: bool = False
    redigir: bool = True
    # Trechos que a redação pelo modelo não pode perder.
    preservar: tuple[str, ...] = ()
