from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base_model import BaseEntity
    
class Client(Document, BaseEntity):
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    disabled: bool = False 

    class Settings:
        name = "clients"

class ClientCreateUpdate(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str

