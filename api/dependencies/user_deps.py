from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from core.config import settings
from fastapi import Body, Depends, HTTPException, status
from typing import Optional
from jose import JWTError, jwt
from models.user import User
from datetime import datetime
from schemas.auth_schema import TokenData, TokenSchema
from services.user_service import UserService

oauth_reusable = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT",
    auto_error=False
)

user_service = UserService()

async def get_current_user(token: str = Depends(oauth_reusable)) -> User:
    if(token ==  None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    token_data = TokenData(**payload)
    if datetime.fromtimestamp(token_data.exp) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
            )     
        
    user = await user_service.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user


