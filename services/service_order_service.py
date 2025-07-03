from typing import List, Dict, Any, Optional
from repositories.service_order_repository import ServiceOrderRepository
from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from repositories.material_repository import MaterialRepository
from schemas.service_order_schema import (
    serviceOrderEntity, 
    list_serviceOrderEntity, 
    ServiceOrderCreateOrUpdate,
    ServiceOrderMaterialCreate,
    ServiceOrderMaterialUpdate,
    ServiceOrderMaterialResponse
)
from models.service_order import ServiceOrder
from core.order_number_generator import OrderNumberGenerator
from datetime import datetime
from beanie import PydanticObjectId


class ServiceOrderService:
    def __init__(self, 
                 service_order_repository: ServiceOrderRepository = None,
                 client_repository: ClientRepository = None,
                 user_repository: UserRepository = None,
                 material_repository: MaterialRepository = None):
        self.service_order_repository = service_order_repository or ServiceOrderRepository()
        self.client_repository = client_repository or ClientRepository()
        self.user_repository = user_repository or UserRepository()
        self.material_repository = material_repository or MaterialRepository()

    async def list_service_orders(self) -> List[Dict[str, Any]]:
        try:
            service_orders = await self.service_order_repository.list_service_orders()
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Erro ao listar ordens de serviço.")

    async def create_service_order(self, service_order_data: ServiceOrderCreateOrUpdate) -> Dict[str, Any]:
        try:        
            # Validate client exists
            client = await self.client_repository.get_client(service_order_data.client_id)    
            if not client:
                raise ValueError("Cliente não encontrado.")
            
            # Validate materials if provided
            if service_order_data.materials:
                await self._validate_and_prepare_materials(service_order_data.materials)
            
            # Generate order number
            service_order_data.order_number = await OrderNumberGenerator.generate_next_order_number()
            service_order_data.created_at = datetime.now()
            service_order_data.client_id = str(client.id)
            
            service_order = ServiceOrder(**dict(service_order_data))

            service_order_db = await self.service_order_repository.create_service_order(service_order)
            return serviceOrderEntity(service_order_db)
        except ValueError as ve:
                raise ve
        except Exception as e:
            raise Exception(f"Erro interno ao criar ordem de serviço: {e}")
    
    async def _validate_and_prepare_materials(self, materials: List) -> None:
        """
        Validates materials and prepares them for service order creation
        """
        for material_data in materials:
            material = await self.material_repository.get_material(material_data.material_id)
            if not material:
                raise ValueError(f"Material com ID {material_data.material_id} não encontrado.")
            
            # If unit price not specified, use the current material price
            if material_data.unit_price is None:
                material_data.unit_price = material.unit_price
            
            # Calculate total price
            material_data.calculate_total_price()

    async def get_service_order(self, service_order_id: str) -> Dict[str, Any]:
        try:
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if service_order:
                return serviceOrderEntity(service_order)
            else:
                raise ValueError("Ordem de serviço não encontrada")
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao buscar ordem de serviço.")

    async def update_service_order(self, service_order_id: str, service_order_data) -> Dict[str, Any]:
        try:
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")

            update_data = service_order_data.dict(exclude_unset=True)

            # Validate assigned user if being updated
            if "assigned_to_id" in update_data:
                assigned_to = await self.user_repository.get_user_by_id(PydanticObjectId(update_data["assigned_to_id"]))
                if not assigned_to:
                    raise ValueError("Usuário atribuído não encontrado")
                update_data["assigned_to"] = assigned_to
                del update_data["assigned_to_id"]

            updated_service_order = await self.service_order_repository.update_service_order(service_order_id, update_data)
            return serviceOrderEntity(updated_service_order)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao atualizar ordem de serviço.")

    async def delete_service_order(self, service_order_id: str) -> Dict[str, str]:
        try:
            result = await self.service_order_repository.delete_service_order(service_order_id)
            if not result:
                raise ValueError("Ordem de serviço não encontrada")
            return {"message": "Ordem de serviço deletada com sucesso"}
        except ValueError as ve:
            raise ve        
        except Exception:
            raise Exception("Erro ao deletar ordem de serviço.")

    async def get_service_orders_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        try:
            service_orders = await self.service_order_repository.get_service_orders_by_client(client_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Erro ao buscar ordens de serviço do cliente.")
        

    async def get_service_orders_by_assigned_user(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            service_orders = await self.service_order_repository.get_service_orders_by_assigned_user(user_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Erro ao buscar ordens de serviço do usuário.")   
        
         
    async def add_material_to_service_order(self, service_order_id: str, material_data: ServiceOrderMaterialCreate) -> Dict[str, Any]:
        """Adds a material to the service order"""
        try:
            # Check if the service order exists
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")
            
            # Check if the material exists
            material = await self.material_repository.get_material(material_data.material_id)
            if not material:
                raise ValueError("Material não encontrado")
            
            # Use the current material price if not specified
            unit_price = material_data.unit_price if material_data.unit_price else material.unit_price
            
            # Add the material
            service_order.add_material(
                material_id=material_data.material_id,
                quantity=material_data.quantity,
                unit_price=unit_price,
                notes=material_data.notes
            )
            
            # Save changes
            updated_service_order = await self.service_order_repository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Erro ao adicionar material à ordem de serviço: {e}")
    
    async def remove_material_from_service_order(self, service_order_id: str, material_id: str) -> Dict[str, Any]:
        """Remove um material da ordem de serviço"""
        try:
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")
            
            # Check if the material exists in the order
            material_exists = any(m.material_id == material_id for m in (service_order.materials or []))
            if not material_exists:
                raise ValueError("Material não encontrado na ordem de serviço")
            
            # Remove the material
            service_order.remove_material(material_id)
            
            # Save changes
            updated_service_order = await self.service_order_repository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Erro ao remover material da ordem de serviço: {e}")
    
    async def update_material_in_service_order(self, service_order_id: str, material_data: ServiceOrderMaterialUpdate) -> Dict[str, Any]:
        """Updates a material in the service order"""
        try:
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")
            
            # Find and update the material
            if not service_order.materials:
                raise ValueError("Material não encontrado na ordem de serviço")
            
            material_found = False
            for material in service_order.materials:
                if material.material_id == material_data.material_id:
                    material_found = True
                    if material_data.quantity is not None:
                        material.quantity = material_data.quantity
                    if material_data.unit_price is not None:
                        material.unit_price = material_data.unit_price
                    if material_data.notes is not None:
                        material.notes = material_data.notes
                    
                    # Recalculate total price
                    material.calculate_total_price()
                    break
            
            if not material_found:
                raise ValueError("Material não encontrado na ordem de serviço")
            
            # Save changes
            updated_service_order = await self.service_order_repository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Erro ao atualizar material na ordem de serviço: {e}")
    
    async def get_service_order_materials_with_details(self, service_order_id: str) -> List[Dict[str, Any]]:
        """Returns service order materials with material details"""
        try:            
            service_order = await self.service_order_repository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")
            
            if not service_order.materials:
                return []
            
            materials_with_details = []
            for service_order_material in service_order.materials:
                material = await self.material_repository.get_material(service_order_material.material_id)
                material_response = ServiceOrderMaterialResponse(
                    material_id=service_order_material.material_id,
                    quantity=service_order_material.quantity,
                    unit_price=service_order_material.unit_price,
                    total_price=service_order_material.total_price,
                    notes=service_order_material.notes,
                    material_name=material.name if material else "Material não encontrado",
                    material_unit=material.unit if material else ""
                )
                materials_with_details.append(material_response.dict())
            
            return materials_with_details
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Erro ao buscar materiais da ordem de serviço: {e}")