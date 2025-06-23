from models.material import Material, MaterialCreateUpdate
from datetime import datetime
from beanie import PydanticObjectId

class MaterialRepository:
    @staticmethod
    async def list_materials():
        return await Material.find_all().to_list()

    @staticmethod
    async def create_material(material: MaterialCreateUpdate):
        material_db = Material(
            **dict(material),
            created_at=datetime.now(),
        )
        await material_db.insert()
        return material_db

    @staticmethod
    async def get_material(material_id):
        return await Material.get(PydanticObjectId(material_id))

    @staticmethod
    async def find_duplicate(code, name, exclude_id=None):
        query = {"$or": [{"code": code}, {"name": name}]}
        if exclude_id:
            query = {"$and": [
                {"_id": {"$ne": PydanticObjectId(exclude_id)}},
                query
            ]}
        return await Material.find_one(query)

    @staticmethod
    async def update_material(material_id, material: MaterialCreateUpdate, created_at):
        update_data = dict(material)
        update_data["updated_at"] = datetime.now()
        update_data["created_at"] = created_at
        await Material.find_one(Material.id == PydanticObjectId(material_id)).set(update_data)
        return await Material.get(PydanticObjectId(material_id))

    @staticmethod
    async def delete_material(material_id):
        material = await Material.get(PydanticObjectId(material_id))
        if material:
            await material.delete()
        return material

    @staticmethod
    async def get_low_stock_materials():
        """Retorna materiais com estoque abaixo do mínimo"""
        return await Material.find(Material.stock_quantity <= Material.minimum_stock).to_list()

    @staticmethod
    async def update_stock(material_id, new_quantity):
        """Atualiza apenas a quantidade em estoque"""
        await Material.find_one(Material.id == PydanticObjectId(material_id)).set({
            "stock_quantity": new_quantity,
            "updated_at": datetime.now()
        })
        return await Material.get(PydanticObjectId(material_id))

    @staticmethod
    async def search_by_category(category):
        """Busca materiais por categoria"""
        return await Material.find(Material.category == category).to_list()