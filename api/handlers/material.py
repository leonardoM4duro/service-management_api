from fastapi import FastAPI, APIRouter, Depends
from services.material_service import MaterialService
from models.material import MaterialCreateUpdate
from models.response_model import ResponseModel
from api.dependencies.user_deps import get_current_user
from pydantic import BaseModel

material_router = APIRouter(dependencies=[Depends(get_current_user)])
service = MaterialService()

class StockUpdateRequest(BaseModel):
    new_quantity: float

@material_router.get('/materials')
async def list_materials():
    try:
        data = await service.list_materials()
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.post('/material')
async def create_material(material: MaterialCreateUpdate):
    try:
        data = await service.create_material(material)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.get('/material/{material_id}')
async def get_material(material_id):
    try:
        data = await service.get_material(material_id)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.put('/material/{material_id}')
async def update_material(material_id, material: MaterialCreateUpdate):
    try:
        data = await service.update_material(material_id, material)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.delete('/material/{material_id}')
async def delete_material(material_id):
    try:
        data = await service.delete_material(material_id)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.get('/materials/low-stock')
async def get_low_stock_materials():
    try:
        data = await service.get_low_stock_materials()
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.patch('/material/{material_id}/stock')
async def update_stock(material_id, stock_request: StockUpdateRequest):
    try:
        data = await service.update_stock(material_id, stock_request.new_quantity)
        return ResponseModel.build(data=data)
    except ValueError as ve:
        return ResponseModel.build(success=False, error=str(ve))
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))

@material_router.get('/materials/category/{category}')
async def search_by_category(category: str):
    try:
        data = await service.search_by_category(category)
        return ResponseModel.build(data=data)
    except Exception as e:
        return ResponseModel.build(success=False, error=str(e))
