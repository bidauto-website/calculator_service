from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService

from app.database.models.destination import Destination
from app.database.models.exchange_rate import ExchangeRate
from app.database.schemas.destination import DestinationCreate, DestinationUpdate
from app.database.schemas.exchange_rate import ExchangeRateCreate, ExchangeRateUpdate
from currency_converter import CurrencyConverter

class ExchangeRateService(BaseService[ExchangeRate, ExchangeRateCreate, ExchangeRateUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(ExchangeRate, session)

    async def get_last_rate(self)-> ExchangeRate:
        result = await self.session.execute(select(ExchangeRate).order_by(ExchangeRate.created_at.desc()).limit(1))
        response = result.scalar_one_or_none()
        currency = CurrencyConverter()
        rate = currency.convert(1, 'USD', 'EUR')

        if not response:
            return await self.create(ExchangeRateCreate(rate=rate))
        else:
            if response.rate != rate:
                response = await self.update(response.id, ExchangeRateUpdate(rate=rate))
        return response







