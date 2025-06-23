from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import client, user, service_order, material
from api.router import router

client_app = [
    "http://localhost:3000",
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    swagger_ui_parameters={
        "docExpansion": "none",  # Mantém todas as tags fechadas
        "defaultModelsExpandDepth": -1,  # Oculta os modelos por padrão
        "defaultModelExpandDepth": -1,   # Oculta detalhes dos modelos
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=client_app,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)   

@app.on_event("startup")
async def startup_event():
    database = AsyncIOMotorClient(settings.MONGODB_URL).serviceManagementSystem
    
    await init_beanie(
        database=database,
        document_models=[
            client.Client,
            user.User,
            service_order.ServiceOrder,
            material.Material,
        ]
    )
