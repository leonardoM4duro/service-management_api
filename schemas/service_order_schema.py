from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.client import Client
from models.user import User
from models.service_order_material import ServiceOrderMaterial
from uuid import UUID

class ServiceOrderCreateOrUpdate(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    client_id: str
    disabled: bool = False
    order_number: Optional[str] = None
    created_at: Optional[datetime] = None
    assigned_to_id: Optional[str] = None
    estimated_hours: Optional[float] = None
    materials: Optional[List[ServiceOrderMaterial]] = [ServiceOrderMaterial]

class ServiceOrderUpdate(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    notes: Optional[List[str]] = None
    materials: Optional[List[ServiceOrderMaterial]] = None

class ServiceOrderMaterialCreate(BaseModel):
    material_id: str
    quantity: float
    unit_price: Optional[float] = None
    notes: Optional[str] = None

class ServiceOrderMaterialUpdate(BaseModel):
    material_id: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None

class ServiceOrderMaterialResponse(BaseModel):
    material_id: str
    quantity: float
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    notes: Optional[str] = None
    material_name: Optional[str] = None  # Para incluir o nome do material nas respostas
    material_unit: Optional[str] = None  # Para incluir a unidade do material

def serviceOrderEntity(db_item) -> dict:
    return {
        "id": str(getattr(db_item, "id", getattr(db_item, "_id", ""))),
        "order_number": getattr(db_item, "order_number", None),
        "title": getattr(db_item, "title", None),
        "description": getattr(db_item, "description", None),
        "status": getattr(db_item, "status", None),
        "client_id": getattr(db_item, "client_id", None),
        "assigned_to_id": getattr(db_item, "assigned_to_id", None),
        "start_date": getattr(db_item, "start_date", None),
        "end_date": getattr(db_item, "end_date", None),
        "estimated_hours": getattr(db_item, "estimated_hours", None),
        "actual_hours": getattr(db_item, "actual_hours", None),
        "notes": getattr(db_item, "notes", None),
        "materials": getattr(db_item, "materials", []),
        "created_at": getattr(db_item, "created_at", None),
        "updated_at": getattr(db_item, "updated_at", None)
    }

def list_serviceOrderEntity(db_items) -> list:
    return [serviceOrderEntity(item) for item in db_items]