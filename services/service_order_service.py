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
            raise Exception("Erro ao listar ordens de serviço.")

    async def create_service_order(self, service_order_data: ServiceOrderCreateOrUpdate):
        try:
            # Validate client exists
            client = await ClientRepository.get_client(service_order_data.client_id)    
            if not client:
                raise ValueError("Cliente não encontrado.")
            
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
            raise Exception(f"Erro interno ao criar ordem de serviço: {e}")

    async def get_service_order(self, service_order_id):
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if service_order:
                return serviceOrderEntity(service_order)
            else:
                raise ValueError("Ordem de serviço não encontrada")
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao buscar ordem de serviço.")

    async def update_service_order(self, service_order_id, service_order_data):
        try:
            service_order = await ServiceOrderRepository.get_service_order(service_order_id)
            if not service_order:
                raise ValueError("Ordem de serviço não encontrada")

            update_data = service_order_data.dict(exclude_unset=True)

            # Validate assigned user if being updated
            if "assigned_to_id" in update_data:
                assigned_to = await UserRepository.get_user_by_id(PydanticObjectId(update_data["assigned_to_id"]))
                if not assigned_to:
                    raise ValueError("Usuário atribuído não encontrado")
                update_data["assigned_to"] = assigned_to
                del update_data["assigned_to_id"]

            updated_service_order = await ServiceOrderRepository.update_service_order(service_order_id, update_data)
            return serviceOrderEntity(updated_service_order)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao atualizar ordem de serviço.")

    async def delete_service_order(self, service_order_id):
        try:
            result = await ServiceOrderRepository.delete_service_order(service_order_id)
            if not result:
                raise ValueError("Ordem de serviço não encontrada")
            return {"message": "Ordem de serviço deletada com sucesso"}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao deletar ordem de serviço.")

    async def get_service_orders_by_client(self, client_id):
        try:
            service_orders = await ServiceOrderRepository.get_service_orders_by_client(client_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Erro ao buscar ordens de serviço do cliente.")

    async def get_service_orders_by_assigned_user(self, user_id):
        try:
            service_orders = await ServiceOrderRepository.get_service_orders_by_assigned_user(user_id)
            return list_serviceOrderEntity(service_orders)
        except Exception:
            raise Exception("Erro ao buscar ordens de serviço do usuário.") 