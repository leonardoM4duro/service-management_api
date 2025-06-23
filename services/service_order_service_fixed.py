from repositories.service_order_repository import ServiceOrderRepository
from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from schemas.service_order_schema import serviceOrderEntity, list_serviceOrderEntity, ServiceOrderCreateOrUpdate
from models.service_order import ServiceOrder
from datetime import datetime
from beanie import PydanticObjectId

class ServiceOrderService:
    async def list_service_orders(self):
        try:
            service_orders = await ServiceOrderRepository.list_service_orders()
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Error listing service orders.")

    async def create_service_order(self, service_order_data: ServiceOrderCreateOrUpdate):
        try:
            from repositories.material_repository import MaterialRepository
            
            # Validate client exists
            client = await ClientRepository.get_client(service_order_data.client_id)    
            if not client:
                raise ValueError("Client not found.")
            
            # Validate materials if provided
            if service_order_data.materials:
                for material_data in service_order_data.materials:
                    material = await MaterialRepository.get_material(material_data.material_id)
                    if not material:
                        raise ValueError(f"Material with ID {material_data.material_id} not found.")
                    
                    # If unit price not specified, use the current material price
                    if material_data.unit_price is None:
                        material_data.unit_price = material.unit_price
                    
                    # Calculate total price
                    material_data.calculate_total_price()
            
            last_order_number = await ServiceOrderRepository.get_last_order_number()
            if last_order_number and last_order_number.startswith("OS-"):
                last_seq = int(last_order_number.split("-")[-1])
                next_seq = last_seq + 1
            else:
                next_seq = 1
                
            service_order_data.order_number = f"OS-{next_seq:04d}"
            service_order_data.created_at = datetime.now()
            service_order_data.client_id = str(client.id)
            
            service_order = ServiceOrder(**dict(service_order_data))

            service_order_db = await ServiceOrderRepository.create_service_order(service_order)
            return serviceOrderEntity(service_order_db)
        except ValueError as ve:
                raise ve
        except Exception as e:
            raise Exception(f"Internal error creating service order: {e}")

    async def get_service_order(self, service_order_id):
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if service_order:
                return serviceOrderEntity(service_order)
            else:
                raise ValueError("Service order not found")
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Error retrieving service order.")

    async def update_service_order(self, service_order_id, service_order_data):
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Service order not found")

            update_data = service_order_data.dict(exclude_unset=True)

            # Validate assigned user if being updated
            if "assigned_to_id" in update_data:
                assigned_to = await UserRepository.get_user_by_id(PydanticObjectId(update_data["assigned_to_id"]))
                if not assigned_to:
                    raise ValueError("Assigned user not found")
                update_data["assigned_to"] = assigned_to
                del update_data["assigned_to_id"]

            updated_service_order = await ServiceOrderRepository.update_service_order(service_order_id, update_data)
            return serviceOrderEntity(updated_service_order)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Internal error updating service order.")

    async def delete_service_order(self, service_order_id):
        try:
            result = await ServiceOrderRepository.delete_service_order(service_order_id)
            if not result:
                raise ValueError("Service order not found")
            return {"message": "Service order deleted successfully"}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Error deleting service order.")

    async def get_service_orders_by_client(self, client_id):
        try:
            service_orders = await ServiceOrderRepository.get_service_orders_by_client(client_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Error retrieving client's service orders.")

    async def get_service_orders_by_assigned_user(self, user_id):
        try:
            service_orders = await ServiceOrderRepository.get_service_orders_by_assigned_user(user_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Error retrieving user's service orders.")
    
    async def add_material_to_service_order(self, service_order_id: str, material_data):
        """Adds a material to the service order"""
        try:
            from repositories.material_repository import MaterialRepository
            
            # Check if the service order exists
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Service order not found")
            
            # Check if the material exists
            material = await MaterialRepository.get_material(material_data.material_id)
            if not material:
                raise ValueError("Material not found")
            
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
            updated_service_order = await ServiceOrderRepository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error adding material to service order: {e}")
    
    async def remove_material_from_service_order(self, service_order_id: str, material_id: str):
        """Removes a material from the service order"""
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Service order not found")
            
            # Check if the material exists in the order
            material_exists = any(m.material_id == material_id for m in (service_order.materials or []))
            if not material_exists:
                raise ValueError("Material not found in service order")
            
            # Remove the material
            service_order.remove_material(material_id)
            
            # Save changes
            updated_service_order = await ServiceOrderRepository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error removing material from service order: {e}")
    
    async def update_material_in_service_order(self, service_order_id: str, material_data):
        """Updates a material in the service order"""
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Service order not found")
            
            # Find and update the material
            if not service_order.materials:
                raise ValueError("Material not found in service order")
            
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
                raise ValueError("Material not found in service order")
            
            # Save changes
            updated_service_order = await ServiceOrderRepository.update_service_order(
                service_order_id, 
                {"materials": service_order.materials}
            )
            
            return serviceOrderEntity(updated_service_order)
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error updating material in service order: {e}")
    
    async def get_service_order_materials_with_details(self, service_order_id: str):
        """Returns the service order materials with material details"""
        try:
            from repositories.material_repository import MaterialRepository
            from schemas.service_order_schema import ServiceOrderMaterialResponse
            
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Service order not found")
            
            if not service_order.materials:
                return []
            
            materials_with_details = []
            for so_material in service_order.materials:
                material = await MaterialRepository.get_material(so_material.material_id)
                material_response = ServiceOrderMaterialResponse(
                    material_id=so_material.material_id,
                    quantity=so_material.quantity,
                    unit_price=so_material.unit_price,
                    total_price=so_material.total_price,
                    notes=so_material.notes,
                    material_name=material.name if material else "Material not found",
                    material_unit=material.unit if material else ""
                )
                materials_with_details.append(material_response.dict())
            
            return materials_with_details
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error retrieving service order materials: {e}")
