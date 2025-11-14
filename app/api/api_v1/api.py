from fastapi import APIRouter

from app.api.api_v1.endpoints.private.exchange_rate import exchange_rate_router
from app.api.api_v1.endpoints.public.calculator import calculator_api_router

public_v1_router = APIRouter(prefix='/v1/public')
private_v1_router = APIRouter(prefix='/private/v1')

public_v1_router.include_router(calculator_api_router)

private_v1_router.include_router(exchange_rate_router)






