from fastapi import APIRouter, Depends, Body
from AuthTools.Permissions.dependencies import require_permissions
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Permissions
from app.database.crud.exchange_rate import ExchangeRateService
from app.database.db.session import get_async_db
from app.database.schemas.exchange_rate import ExchangeRateCreate
from app.schemas.exchange_rate import ExchangeRateIn

exchange_rate_router = APIRouter(prefix='/exchange-rate')


@exchange_rate_router.post("", dependencies=[Depends(require_permissions(Permissions.EXCHANGE_RATE_WRITE))])
async def edit_exchange_rate(data: ExchangeRateIn = Body(...),db: AsyncSession = Depends(get_async_db)):
    exchange_rate_service = ExchangeRateService(db)
    response = await exchange_rate_service.create(ExchangeRateCreate(rate=data.rate))
    return response








