from beanie import Document, Indexed
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .base_model import BaseEntity
from .Enums.ServiceOrderStatus import ServiceOrderStatus


class ServiceOrder(Document, BaseEntity):
    order_number: Indexed(str, unique=True)
    title: str
    description: str
    status: ServiceOrderStatus = ServiceOrderStatus.OPEN
    client_id: str
    assigned_to_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    notes: Optional[List[str]] = []
    
    def __repr__(self) -> str:
        return f"ServiceOrder(order_number={self.order_number}, status={self.status})"
    
    def __str__(self) -> str:
        return f"OS-{self.order_number}"
    
    class Settings:
        name = "service_orders" 