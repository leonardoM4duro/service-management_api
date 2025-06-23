from fastapi import APIRouter
from .handlers import client, user, service_order, material
from .auth import jwt_auth

router = APIRouter()

router.include_router(client.client_router, prefix="/clients", tags=["Clients"])
router.include_router(user.user_router, prefix="/users", tags=["Users"])
router.include_router(service_order.service_order_router, prefix="/service-orders", tags=["Service Orders"])
router.include_router(material.material_router, prefix="/materials", tags=["Materials"])
router.include_router(jwt_auth.auth_router, prefix="/auth", tags=["Authentication"])