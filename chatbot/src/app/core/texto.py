import re
import unicodedata
from datetime import date, datetime, time

DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


def sem_acentos(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos e sem pontuação, para comparar textos."""
    texto = re.sub(r"[^\w\s]", " ", sem_acentos(texto).lower())
    return re.sub(r"\s+", " ", texto).strip()


def formatar_data(dia: date) -> str:
    return f"{DIAS_SEMANA[dia.weekday()]}, {dia:%d/%m}"


def formatar_hora(hora: time) -> str:
    return f"{hora:%Hh%M}"


def formatar_data_hora(momento: datetime) -> str:
    return f"{formatar_data(momento.date())}, às {formatar_hora(momento.time())}"


def formatar_preco(valor: float) -> str:
    inteiro, centavos = f"{valor:,.2f}".split(".")
    return f"R$ {inteiro.replace(',', '.')},{centavos}"
