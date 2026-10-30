from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.errors import registrar_tratadores
from app.api.health import router as health_router

app = FastAPI(
    title="PetCare Hub Chatbot",
    description="Serviço conversacional do PetCare Hub.",
    version="0.1.0",
)

registrar_tratadores(app)
app.include_router(health_router)
app.include_router(chat_router)
