from typing import Optional
from repositories.service_order_repository import ServiceOrderRepository


class OrderNumberGenerator:
    """Generator for service order numbers"""
    
    ORDER_PREFIX = "OS"
    ORDER_FORMAT = "{prefix}-{sequence:04d}"
    
    @classmethod
    async def generate_next_order_number(cls) -> str:
        """
        Generates the next sequential order number
        
        Returns:
            str: Next order number in format OS-XXXX
        """
        last_order_number = await ServiceOrderRepository.get_last_order_number()
        next_sequence = cls._calculate_next_sequence(last_order_number)
        
        return cls.ORDER_FORMAT.format(
            prefix=cls.ORDER_PREFIX,
            sequence=next_sequence
        )
    
    @classmethod
    def _calculate_next_sequence(cls, last_order_number: Optional[str]) -> int:
        """
        Calculates the next sequence number based on the last order number
        """
        if not last_order_number or not last_order_number.startswith(f"{cls.ORDER_PREFIX}-"):
            return 1
            
        try:
            last_sequence = int(last_order_number.split("-")[-1])
            return last_sequence + 1
        except (ValueError, IndexError):
            return 1
    
    @classmethod
    def validate_order_number_format(cls, order_number: str) -> bool:
        """
        Validates if an order number follows the expected format
        """
        if not order_number:
            return False
            
        parts = order_number.split("-")
        if len(parts) != 2:
            return False
            
        prefix, sequence = parts
        if prefix != cls.ORDER_PREFIX:
            return False
            
        try:
            sequence_num = int(sequence)
            return sequence_num > 0 and len(sequence) == 4
        except ValueError:
            return False
