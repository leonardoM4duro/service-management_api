from repositories.client_repository import ClientRepository
from schemas.client_schema import clientEntity, list_clientEntity
from datetime import datetime

class ClientService:
    async def list_clients(self):
        try:
            clients = await ClientRepository.list_clients()
            return list_clientEntity(clients)
        except Exception:
            raise Exception("Erro ao listar clientes.")

    async def create_client(self, client):
        try:
            duplicate = await ClientRepository.find_duplicate(client.email, client.phone)
            if duplicate:
                raise ValueError("Já existe um cliente com este e-mail ou telefone.")
            client_db = await ClientRepository.create_client(client)
            return await self.list_clients()
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao criar cliente.")

    async def get_client(self, client_id):
        try:
            client = await ClientRepository.get_client(client_id)
            if client:
                return clientEntity(client)
            else:
                raise ValueError("Client not found")
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao buscar cliente.")

    async def update_client(self, client_id, client):
        try:
            client_db = await ClientRepository.get_client(client_id)
            if not client_db:
                raise ValueError("Client not found")
            duplicate = await ClientRepository.find_duplicate(client.email, client.phone, exclude_id=client_id)
            if duplicate:
                raise ValueError("Já existe outro cliente com este e-mail ou telefone.")
            updated_client = await ClientRepository.update_client(client_id, client, client_db.created_at)
            return clientEntity(updated_client)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro interno ao atualizar cliente.")

    async def delete_client(self, client_id):
        try:
            client = await ClientRepository.delete_client(client_id)
            if not client:
                raise ValueError("Client not found")
            return {"message": "Client deleted successfully"}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception("Erro ao deletar cliente.")
