
from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema, TokenData
from api.dependencies.user_deps import get_current_user
from models.user import User
from schemas.user_schema import UserResponse
from jose import JWTError, jwt
from core.config import settings
from fastapi import Body

auth_router = APIRouter()

@auth_router.post("/login", summary="Login to get access token", response_model=TokenSchema)
async def login(data : OAuth2PasswordRequestForm = Depends()):
    user = await UserService.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    
    return {
        "access_token": create_access_token(user.id), 
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer"
    }
    
@auth_router.post("/test-token", summary="Test token", response_model=UserResponse)
async def test_token(user: User = Depends(get_current_user)):   
    return user

@auth_router.post("/refresh-token", summary="Refresh access token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)) -> TokenSchema:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }