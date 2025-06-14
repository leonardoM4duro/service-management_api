from passlib.context import CryptContext
from typing import Union, Any
from core.config import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data: Union[str, dict], expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    info_jwt = {
        "exp": expires_delta,
        "sub": str(data),
    }
    jwt_encoded =  jwt.encode(info_jwt, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded


def create_refresh_token(data: Union[str, dict], expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_REFRESH_TOKEN_SECRET_KEY)
        
    info_jwt = {
        "exp": expires_delta,
        "sub": str(data),
    }
    jwt_encoded =  jwt.encode(info_jwt, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded