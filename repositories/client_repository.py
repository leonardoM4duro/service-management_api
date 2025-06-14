from models.client import Client, ClientCreateUpdate
from datetime import datetime
from beanie import PydanticObjectId

class ClientRepository:
    @staticmethod
    async def list_clients():
        return await Client.find_all().to_list()

    @staticmethod
    async def create_client(client: ClientCreateUpdate):
        client_db = Client(
            **dict(client),
            created_at=datetime.now(),
        )
        await client_db.insert()
        return client_db

    @staticmethod
    async def get_client(client_id):
        return await Client.get(PydanticObjectId(client_id))

    @staticmethod
    async def find_duplicate(email, phone, exclude_id=None):
        query = {"$or": [{"email": email}, {"phone": phone}]}
        if exclude_id:
            query = {"$and": [
                {"_id": {"$ne": PydanticObjectId(exclude_id)}},
                query
            ]}
        return await Client.find_one(query)

    @staticmethod
    async def update_client(client_id, client: ClientCreateUpdate, created_at):
        update_data = dict(client)
        update_data["updated_at"] = datetime.now()
        update_data["created_at"] = created_at
        await Client.find_one(Client.id == PydanticObjectId(client_id)).set(update_data)
        return await Client.get(PydanticObjectId(client_id))

    @staticmethod
    async def delete_client(client_id):
        client = await Client.get(PydanticObjectId(client_id))
        if client:
            await client.delete()
        return client
