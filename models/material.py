from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base_model import BaseEntity
    
class Material(Document, BaseEntity):
    name: str
    description: str
    unit: str  # unit of measurement (kg, m, l, etc.)
    unit_price: float
    stock_quantity: float
    minimum_stock: float
    unit_price: float
    category: str
    code: str  # internal material code
    disabled: bool = False 

    class Settings:
        name = "materials"

class MaterialCreateUpdate(BaseModel):
    name: str
    description: str
    unit: str
    unit_price: float
    stock_quantity: float
    minimum_stock: float
    category: str
    code: Optional[str] = None
