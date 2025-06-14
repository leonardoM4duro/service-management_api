from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from .base_model import BaseEntity

class User(Document, BaseEntity):
    name : Indexed(str)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hash_password: str
    disabled: bool = False
    
    def __repr__(self) -> str:
        return f"User(username={self.username}, email={self.email})"
    
    def __str__(self) -> str:
        return self.email
    
    def __hash__(self) -> int:
        return hash(self.email)
                    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return self.email == other.email
        return False
    
    class Settings:
        name = "users"