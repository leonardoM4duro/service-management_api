from decouple import config
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings): 
    
    PROJECT_NAME: str = "Service Management System"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A FastAPI project template"
    PROJECT_URL: AnyHttpUrl = "http://localhost:8000"
    PROJECT_BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000"
    ]
    # database settings
    MONGODB_URL: str = config("MONGODB_URI", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 480    
    SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    ACCESS_REFRESH_TOKEN_SECRET_KEY: int = 120    
    REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    
settings = Settings()