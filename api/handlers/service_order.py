from fastapi import APIRouter, Depends, Path
from models.user import User
from services.service_order_service import ServiceOrderService
from schemas.service_order_schema import ServiceOrderCreateOrUpdate, ServiceOrderUpdate
from models.response_model import ResponseModel
from api.dependencies.user_deps import get_current_user

service_order_router = APIRouter(dependencies=[Depends(get_current_user)])
service = ServiceOrderService()

@service_order_router.get('/service-orders')
async def list_service_orders():
    try:
        data = await service.list_service_orders()
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.post('/service-orders')
async def create_service_order(service_order: ServiceOrderCreateOrUpdate, current_user: User = Depends(get_current_user)):
    try:
        service_order.assigned_to_id = str(current_user.id)
        data = await service.create_service_order(service_order)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.get('/service-orders/{service_order_id}')
async def get_service_order(service_order_id: str = Path(...)):
    try:
        data = await service.get_service_order(service_order_id)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.put('/service-orders/{service_order_id}')
async def update_service_order(
    service_order: ServiceOrderUpdate,
    service_order_id: str = Path(...)
):
    try:
        data = await service.update_service_order(service_order_id, service_order)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.delete('/service-orders/{service_order_id}')
async def delete_service_order(service_order_id: str = Path(...)):
    try:
        data = await service.delete_service_order(service_order_id)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.get('/clients/{client_id}/service-orders')
async def get_service_orders_by_client(client_id: str = Path(...)):
    try:
        data = await service.get_service_orders_by_client(client_id)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@service_order_router.get('/users/{user_id}/service-orders')
async def get_service_orders_by_assigned_user(user_id: str = Path(...)):
    try:
        data = await service.get_service_orders_by_assigned_user(user_id)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e)) 