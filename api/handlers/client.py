from fastapi import FastAPI, APIRouter, Depends
from services.client_service import ClientService
from models.client import ClientCreateUpdate
from models.response_model import ResponseModel
from api.dependencies.user_deps import get_current_user

client_router = APIRouter(dependencies=[Depends(get_current_user)])
service = ClientService()

@client_router.get('/clients')
async def list_clients():
    try:
        data = await service.list_clients()
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@client_router.post('/client')
async def create_client(client: ClientCreateUpdate):
    try:
        data = await service.create_client(client)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@client_router.get('/client/{client_id}')
async def get_client(client_id):
    try:
        data = await service.get_client(client_id)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@client_router.put('/client/{client_id}')
async def update_client(client_id, client: ClientCreateUpdate):
    try:
        data = await service.update_client(client_id, client)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@client_router.delete('/client/{client_id}')
async def delete_client(client_id):
    try:
        data = await service.delete_client(client_id)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))



