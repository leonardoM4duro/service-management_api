from typing import Dict, List, Any
from repositories.material_repository import MaterialRepository
from schemas.material_schema import materialEntity, list_materialEntity
from core.constants import ErrorMessages, SuccessMessages, ValidationConfig


class MaterialService:
    def __init__(self, material_repository: MaterialRepository = None):
        self.repository = material_repository or MaterialRepository()
    async def list_materials(self) -> List[Dict[str, Any]]:
        # Lists all registered materials
        try:
            materials = await self.repository.list_materials()
            return list_materialEntity(materials)
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_LIST_ERROR)

    async def create_material(self, material) -> List[Dict[str, Any]]:
        # Creates a new material after validations
        try:
            # Automatically generates the material code
            material.code = await self._generate_material_code(material.name)
            
            if await self.repository.validate_duplicate_material(material.name):
                raise ValueError(ErrorMessages.MATERIAL_DUPLICATE_CODE_NAME)
            await self.repository.create_material(material)
            return await self.list_materials()
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_CREATE_ERROR)

    async def get_material(self, material_id: str) -> Dict[str, Any]:
        # Searches for a specific material by ID
        try:
            material = await self._get_material_by_id(material_id)
            return materialEntity(material)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_GET_ERROR)

    async def update_material(self, material_id: str, material) -> Dict[str, Any]:
        # Updates data of an existing material
        try:
            material_db = await self._get_material_by_id(material_id)
            
            # Preserves the original code - does not allow modification
            material.code = material_db.code
            
            if await self.repository.validate_duplicate_material(material.name, material_id):
                raise ValueError(ErrorMessages.MATERIAL_DUPLICATE_CODE_NAME)
            updated_material = await self.repository.update_material(material_id, material, material_db.created_at)
            return materialEntity(updated_material)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_UPDATE_ERROR)

    async def delete_material(self, material_id: str) -> Dict[str, str]:
        # Removes a material from the system
        try:
            result = await self.repository.delete_material(material_id)
            if not result:
                raise ValueError(ErrorMessages.MATERIAL_NOT_FOUND)
            return {"message": SuccessMessages.MATERIAL_DELETED}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_DELETE_ERROR)

    async def get_low_stock_materials(self) -> List[Dict[str, Any]]:
        # Lists materials with low stock
        try:
            materials = await self.repository.get_low_stock_materials()
            return list_materialEntity(materials)
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_LOW_STOCK_ERROR)

    async def update_stock(self, material_id: str, new_quantity: int) -> Dict[str, Any]:
        # Updates the stock of a material
        try:
            self._validate_stock_quantity(new_quantity)
            material = await self._get_material_by_id(material_id)
            updated_material = await self.repository.update_stock(material.id, new_quantity)
            return materialEntity(updated_material)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_UPDATE_STOCK_ERROR)

    async def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        # Searches for materials by category
        try:
            materials = await self.repository.search_by_category(category)
            return list_materialEntity(materials)
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_SEARCH_CATEGORY_ERROR)

    async def _get_material_by_id(self, material_id: str):
        # Searches for material by ID with existence validation
        material = await self.repository.get_material(material_id)
        if not material:
            raise ValueError(ErrorMessages.MATERIAL_NOT_FOUND)
        return material

    def _validate_stock_quantity(self, quantity: int):
        # Validates if the stock quantity is valid
        if quantity < ValidationConfig.MIN_STOCK_LEVEL:
            raise ValueError(ErrorMessages.MATERIAL_NEGATIVE_QUANTITY)
    
    async def _generate_material_code(self, name: str) -> str:
        # Generates automatic code based on the first two letters of the name + sequential number
        try:
            # Gets the first two letters of the name in uppercase
            prefix = name[:2].upper()
            
            # Counts how many materials already exist with this prefix
            count = await self.repository.count_materials_by_prefix(prefix)
            
            # Generates the next sequential number (with 3 digits)
            next_number = count + 1
            code = f"{prefix}{next_number:03d}"
            
            return code
        except Exception:
            raise Exception(ErrorMessages.MATERIAL_CODE_GENERATE_ERROR)
