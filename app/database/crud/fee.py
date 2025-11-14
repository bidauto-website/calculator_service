from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import Fee, FeeType
from app.database.schemas.fee import FeeCreate, FeeUpdate


class FeeService(BaseService[Fee, FeeCreate, FeeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Fee, session)

    async def get_by_fee_type(self, fee_type: FeeType)-> Sequence[Fee]:
        result = await self.session.execute(select(Fee).where(Fee.fee_type == fee_type))
        return result.scalars().all()

    async def get_fee_in_car_price(self, fee_type: FeeType, price: int)-> Fee | None:
        result = await self.session.execute(
            select(Fee).where(
                Fee.fee_type == fee_type,
                and_(
                    Fee.car_price_min <= price,
                    Fee.car_price_max >= price
                )
            )
            .order_by(Fee.car_price_min)
            .limit(1)
        )
        print(result)
        return result.scalar_one_or_none()




