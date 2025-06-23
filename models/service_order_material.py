from pydantic import BaseModel
from typing import Optional

class ServiceOrderMaterial(BaseModel):
    material_id: str
    quantity: float
    unit_price: Optional[float] = None  # preço unitário na época da ordem de serviço
    total_price: Optional[float] = None  # quantidade * unit_price
    notes: Optional[str] = None  # observações específicas do material nesta ordem
    
    def calculate_total_price(self) -> float:
        """Calcula o preço total baseado na quantidade e preço unitário"""
        if self.unit_price is not None:
            self.total_price = self.quantity * self.unit_price
            return self.total_price
        return 0.0
