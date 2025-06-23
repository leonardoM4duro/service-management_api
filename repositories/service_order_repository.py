from models.service_order import ServiceOrder
from models.client import Client
from models.user import User
from datetime import datetime
from beanie import PydanticObjectId
from typing import Optional, List

class ServiceOrderRepository:
    @staticmethod
    async def list_service_orders():
        return await ServiceOrder.find_all().to_list()

    @staticmethod
    async def create_service_order(service_order: ServiceOrder):
        await service_order.insert()
        return service_order

    @staticmethod
    async def get_service_order(service_order_id: str):
        return await ServiceOrder.get(PydanticObjectId(service_order_id))

    @staticmethod
    async def get_service_order_by_number(order_number: str):
        return await ServiceOrder.find_one(ServiceOrder.order_number == order_number)

    @staticmethod
    async def update_service_order(service_order_id: str, update_data: dict):
        service_order = await ServiceOrder.get(PydanticObjectId(service_order_id))
        if service_order:
            update_data["updated_at"] = datetime.now()
            await service_order.update({"$set": update_data})
            return await ServiceOrder.get(PydanticObjectId(service_order_id))
        return None

    @staticmethod
    async def delete_service_order(service_order_id: str):
        service_order = await ServiceOrder.get(PydanticObjectId(service_order_id))
        if service_order:
            await service_order.delete()
            return True
        return False

    @staticmethod
    async def get_service_orders_by_client(client_id: str):
        return await ServiceOrder.find(ServiceOrder.client.id == PydanticObjectId(client_id)).to_list()

    @staticmethod
    async def get_service_orders_by_assigned_user(user_id: str):
        return await ServiceOrder.find(ServiceOrder.assigned_to.id == PydanticObjectId(user_id)).to_list()

    @staticmethod
    async def get_last_order_number():
        # Busca a última ordem de serviço pelo maior número sequencial
        last_order = await ServiceOrder.find().sort("-order_number").limit(1).to_list()
        if last_order:
            return last_order[0].order_number
        return None 