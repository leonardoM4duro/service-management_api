from typing import Dict, List, Any
from repositories.client_repository import ClientRepository
from schemas.client_schema import clientEntity, list_clientEntity
from core.constants import ErrorMessages, SuccessMessages


class ClientService:
    def __init__(self, client_repository: ClientRepository = None):
        self.repository = client_repository or ClientRepository()

    async def list_clients(self) -> List[Dict[str, Any]]:
        # Lists all registered clients
        try:
            clients = await self.repository.list_clients()
            return list_clientEntity(clients)
        except Exception:
            raise Exception(ErrorMessages.CLIENT_LIST_ERROR)

    async def create_client(self, client) -> List[Dict[str, Any]]:
        # Creates a new client after validations
        try:
            await self._validate_duplicate_client(client.email, client.phone)
            await self.repository.create_client(client)
            return await self.list_clients()
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.CLIENT_CREATE_ERROR)

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        # Gets a specific client by ID
        try:
            client = await self._get_client_by_id(client_id)
            return clientEntity(client)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.CLIENT_GET_ERROR)

    async def update_client(self, client_id: str, client) -> Dict[str, Any]:
        # Updates existing client data
        try:
            client_db = await self._get_client_by_id(client_id)
            await self._validate_duplicate_client(client.email, client.phone, client_id)
            updated_client = await self.repository.update_client(client_id, client, client_db.created_at)
            return clientEntity(updated_client)
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.CLIENT_UPDATE_ERROR)

    async def delete_client(self, client_id: str) -> Dict[str, str]:
        # Removes a client from the system
        try:
            result = await self.repository.delete_client(client_id)
            if not result:
                raise ValueError(ErrorMessages.CLIENT_NOT_FOUND)
            return {"message": SuccessMessages.CLIENT_DELETED}
        except ValueError as ve:
            raise ve
        except Exception:
            raise Exception(ErrorMessages.CLIENT_DELETE_ERROR)

    async def _get_client_by_id(self, client_id: str):
        # Gets client by ID with existence validation
        client = await self.repository.get_client(client_id)
        if not client:
            raise ValueError(ErrorMessages.CLIENT_NOT_FOUND)
        return client

    async def _validate_duplicate_client(self, email: str, phone: str, exclude_id: str = None):
        # Validates if client with same email or phone already exists
        duplicate = await self.repository.find_duplicate(email, phone, exclude_id=exclude_id)
        if duplicate:
            raise ValueError(ErrorMessages.CLIENT_DUPLICATE_EMAIL_PHONE)
