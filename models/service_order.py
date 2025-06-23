from beanie import Document
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .base_model import BaseEntity
from .Enums.ServiceOrderStatus import ServiceOrderStatus
from .service_order_material import ServiceOrderMaterial


class ServiceOrder(Document, BaseEntity):
    order_number: str = Field(..., unique=True)
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
    materials: Optional[List[ServiceOrderMaterial]] = []
    
    def __repr__(self) -> str:
        return f"ServiceOrder(order_number={self.order_number}, status={self.status})"
    
    def __str__(self) -> str:
        return f"OS-{self.order_number}"
    
    class Settings:
        name = "service_orders"
        
    def calculate_total_materials_cost(self) -> float:
        """Calcula o custo total de todos os materiais da ordem de serviço"""
        total_cost = 0.0
        if self.materials:
            for material in self.materials:
                total_cost += material.calculate_total_price()
        return total_cost
    
    def add_material(self, material_id: str, quantity: float, unit_price: Optional[float] = None, notes: Optional[str] = None):
        """Adiciona um material à ordem de serviço"""
        if not self.materials:
            self.materials = []
        
        new_material = ServiceOrderMaterial(
            material_id=material_id,
            quantity=quantity,
            unit_price=unit_price,
            notes=notes
        )
        new_material.calculate_total_price()
        self.materials.append(new_material)
    
    def remove_material(self, material_id: str):
        """Remove um material da ordem de serviço"""
        if self.materials:
            self.materials = [m for m in self.materials if m.material_id != material_id]