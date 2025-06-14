from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name : str
    email: EmailStr
    
class UserUpdate(BaseModel):
    id: str
    name : str
    email: EmailStr
    
    
class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    email: EmailStr

    @staticmethod
    def from_user(user):
        return UserResponse(
            id=str(user.id),
            name=user.name,
            username=user.username,
            email=user.email
        )
