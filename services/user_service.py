from models.user import User
from schemas.user_schema import UserCreate, UserUpdate,UserResponse
from typing import List, Optional
from beanie import PydanticObjectId
from core.security import create_password, verify_password
from repositories.user_repository import UserRepository
from schemas.user_schema import UserResponse

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserResponse:
        existing_user = await User.find_one(User.email == user_data.email)
        if existing_user:
            raise ValueError("Já existe um usuário com este e-mail.")
        user_dict = user_data.dict()

        name_parts = user_dict["name"].strip().split()
        if len(name_parts) >= 2:
            username = f"{name_parts[0].lower()}.{name_parts[-1].lower()}"
        else:
            username = name_parts[0].lower()
            
        hashed_password = create_password(username)
            
        user_dict["username"] = username
        user_dict["hash_password"] = hashed_password
        user = User(**user_dict)
        
        user = await UserRepository.insert_user(user)
        return UserResponse.from_user(user)

    @staticmethod
    async def get_user_by_id(user_id: PydanticObjectId) -> Optional[UserResponse]:
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            return UserResponse.from_user(user)
        return None

    @staticmethod
    async def get_all_users() -> List[UserResponse]:
        users = await UserRepository.get_all_users()
        return [UserResponse.from_user(user) for user in users]

    @staticmethod
    async def update_user(user_data: UserUpdate) -> Optional[UserResponse]:
        user = await UserRepository.get_user_by_id(user_data.id)
        if user:
            existing_user = await User.find_one(User.email == user_data.email, User.id != user_data.id)
            if existing_user:
                raise ValueError("Já existe outro usuário com este e-mail.")
            
            user.name = user_data.name
            user.email = user_data.email            
            user = await UserRepository.update_user(user)
            return UserResponse.from_user(user)
        return None

    @staticmethod
    async def delete_user(user_id: PydanticObjectId) -> bool:
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            await UserRepository.delete_user(user)
            return True
        return False
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserResponse]:
        user = await UserRepository.get_user_by_email(email)
        if user:
            return UserResponse.from_user(user)
        return None
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[UserResponse]:
        user = await UserRepository.get_user_by_username(email)
        if user and verify_password(password, user.hash_password):
            return UserResponse.from_user(user)
        return None

    @staticmethod
    async def get_user_by_id(id: str) -> Optional[UserResponse]:
        user = await UserRepository.get_user_by_id(PydanticObjectId(id))
        return user