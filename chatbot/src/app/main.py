from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.errors import registrar_tratadores
from app.api.health import router as health_router
from app.services.chat_service import chat_service


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    yield
    await chat_service.backend.fechar()


app = FastAPI(
    title="PetCare Hub Chatbot",
    description="Serviço conversacional do PetCare Hub.",
    version="0.1.0",
    lifespan=ciclo_de_vida,
)

registrar_tratadores(app)
app.include_router(health_router)
app.include_router(chat_router)
