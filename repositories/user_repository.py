from models.user import User
from typing import List, Optional
from beanie import PydanticObjectId

class UserRepository:
    @staticmethod
    async def insert_user(user: User) -> User:
        await user.insert()
        return user

    @staticmethod
    async def get_user_by_id(user_id: PydanticObjectId) -> Optional[User]:
        return await User.get(user_id)

    @staticmethod
    async def get_all_users() -> List[User]:
        return await User.find_all().to_list()

    @staticmethod
    async def update_user(user: User) -> User:
        await user.save()
        return user

    @staticmethod
    async def delete_user(user: User) -> bool:
        await user.delete()
        return True
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        return await User.find_one(User.username == username)
