from repositories.material_repository import MaterialRepository
from schemas.material_schema import materialEntity, list_materialEntity
from datetime import datetime

class MaterialService:
    async def list_materials(self):
        try:
            materials = await MaterialRepository.list_materials()
            return list_materialEntity(materials)
        except Exception:
            raise Exception("Erro ao listar materiais.")

    async def create_material(self, material):
        try:
            # Verifica se já existe material com mesmo código ou nome
            duplicate = await MaterialRepository.find_duplicate(material.code, material.name)
            if duplicate:
                raise ValueError("Já existe um material com este código ou nome.")
            await MaterialRepository.create_material(material)
            return await self.list_materials()
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao criar material.")

    async def get_material(self, material_id):
        try:
            material = await MaterialRepository.get_material(material_id)
            if material:
                return materialEntity(material)
            else:
                raise ValueError("Material não encontrado")
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao buscar material.")

    async def update_material(self, material_id, material):
        try:
            material_db = await MaterialRepository.get_material(material_id)
            if not material_db:
                raise ValueError("Material não encontrado")
            
            # Verifica duplicatas excluindo o próprio material
            duplicate = await MaterialRepository.find_duplicate(material.code, material.name, exclude_id=material_id)
            if duplicate:
                raise ValueError("Já existe outro material com este código ou nome.")
            
            updated_material = await MaterialRepository.update_material(material_id, material, material_db.created_at)
            return materialEntity(updated_material)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao atualizar material.")

    async def delete_material(self, material_id):
        try:
            material = await MaterialRepository.delete_material(material_id)
            if not material:
                raise ValueError("Material não encontrado")
            return {"message": "Material deletado com sucesso"}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao deletar material.")

    async def get_low_stock_materials(self):
        try:
            materials = await MaterialRepository.get_low_stock_materials()
            return list_materialEntity(materials)
        except Exception:
            raise Exception("Erro ao buscar materiais com estoque baixo.")

    async def update_stock(self, material_id, new_quantity):
        try:
            if new_quantity < 0:
                raise ValueError("A quantidade não pode ser negativa.")
            
            material = await MaterialRepository.get_material(material_id)
            if not material:
                raise ValueError("Material não encontrado")
            
            updated_material = await MaterialRepository.update_stock(material_id, new_quantity)
            return materialEntity(updated_material)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao atualizar estoque.")

    async def search_by_category(self, category):
        try:
            materials = await MaterialRepository.search_by_category(category)
            return list_materialEntity(materials)
        except Exception:
            raise Exception("Erro ao buscar materiais por categoria.")
