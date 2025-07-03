from models.user import User
from schemas.user_schema import UserCreate, UserUpdate,UserResponse
from typing import List, Optional
from beanie import PydanticObjectId
from core.security import create_password, verify_password
from repositories.user_repository import UserRepository
from schemas.user_schema import UserResponse

class UserService:
    def __init__(self, user_repository: UserRepository = None):
        self.repository = user_repository or UserRepository()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
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
        
        user = await self.repository.insert_user(user)
        return UserResponse.from_user(user)

    async def get_user_by_id(self, user_id: PydanticObjectId) -> Optional[UserResponse]:
        user = await self.repository.get_user_by_id(user_id)
        if user:
            return UserResponse.from_user(user)
        return None

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.repository.get_all_users()
        return [UserResponse.from_user(user) for user in users]

    async def update_user(self, user_data: UserUpdate) -> Optional[UserResponse]:
        user = await self.repository.get_user_by_id(user_data.id)
        if user:
            existing_user = await User.find_one(User.email == user_data.email, User.id != user_data.id)
            if existing_user:
                raise ValueError("Já existe outro usuário com este e-mail.")
            
            user.name = user_data.name
            user.email = user_data.email            
            user = await self.repository.update_user(user)
            return UserResponse.from_user(user)
        return None

    async def delete_user(self, user_id: PydanticObjectId) -> bool:
        user = await self.repository.get_user_by_id(user_id)
        if user:
            await self.repository.delete_user(user)
            return True
        return False
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self.repository.get_user_by_email(email)
        if user:
            return UserResponse.from_user(user)
        return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        user = await self.repository.get_user_by_username(email)
        if user and verify_password(password, user.hash_password):
            return UserResponse.from_user(user)
        return None

    async def get_user_by_id(self, id: str) -> Optional[UserResponse]:
        user = await self.repository.get_user_by_id(PydanticObjectId(id))
        return user