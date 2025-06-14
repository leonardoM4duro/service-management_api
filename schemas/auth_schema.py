from pydantic import BaseModel, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenData(BaseModel):
    sub: str = None
    exp: int = None