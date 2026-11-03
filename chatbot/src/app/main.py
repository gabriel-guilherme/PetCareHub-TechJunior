from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="PetCare Hub Chatbot",
    description="Serviço conversacional do PetCare Hub.",
    version="0.1.0",
)

app.include_router(health_router)
