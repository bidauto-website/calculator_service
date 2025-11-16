from fastapi import APIRouter

from app.api.api_v1.endpoints.public.calculator import calculator_api_router

public_v1_router = APIRouter(prefix='/public')

public_v1_router.include_router(calculator_api_router)