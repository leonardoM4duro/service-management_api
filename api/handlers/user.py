from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from beanie import PydanticObjectId
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from models.user import User
from services.user_service import UserService
from models.response_model import ResponseModel
from api.dependencies.user_deps import get_current_user


user_router = APIRouter(dependencies=[Depends(get_current_user)])

@user_router.post("/user", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        created_user = await UserService.create_user(user)
        return ResponseModel.build(data=created_user)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error="Erro interno ao criar usuário.")

@user_router.get("/users", response_model=ResponseModel)
async def get_all_users():
    try:
        users = await UserService.get_all_users()
        return ResponseModel.build(data=users)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@user_router.get("/user/{user_id}", response_model=ResponseModel)
async def get_user_by_id(user_id: PydanticObjectId):
    try:
        user = await UserService.get_user_by_id(user_id)
        if not user:
            return ResponseModel.build(success=False, error="User not found")
        return ResponseModel.build(data=user)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@user_router.put("/user", response_model=ResponseModel)
async def update_user(user: UserUpdate):
    try:
        updated_user = await UserService.update_user(user)
        if not updated_user:
            return ResponseModel.build(success=False, error="User not found")
        return ResponseModel.build(data=updated_user)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error="Erro interno ao atualizar usuário.")

@user_router.delete("/user/{user_id}", response_model=ResponseModel)
async def delete_user(user_id: PydanticObjectId):
    try:
        deleted = await UserService.delete_user(user_id)
        if not deleted:
            return ResponseModel.build(success=False, error="User not found")
        return ResponseModel.build(success=True)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))
    
@user_router.get("/current_user", summary="Get current user information", response_model=ResponseModel)
async def get_me(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    return ResponseModel.build(data=UserResponse.from_user(user))
    
