from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import AdditionalFee
from app.database.schemas.additional_fee import AdditionalFeeCreate, AdditionalFeeUpdate


class AdditionalFeeService(BaseService[AdditionalFee, AdditionalFeeCreate, AdditionalFeeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(AdditionalFee, session)

    async def get_price_in_int_proxy(self, price: int) -> AdditionalFee | None:
        result = await self.session.execute(
            select(AdditionalFee).where(
                AdditionalFee.int_proxy_min.is_not(None),
                AdditionalFee.int_proxy_max.is_not(None),
                AdditionalFee.int_proxy_min <= price,
                AdditionalFee.int_proxy_max >= price
            )
            .order_by(AdditionalFee.int_proxy_min)
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def  get_price_in_live(self, price: int)-> AdditionalFee | None:
        result = await self.session.execute(
            select(AdditionalFee).where(
                AdditionalFee.live_bid_min.is_not(None),
                AdditionalFee.live_bid_max.is_not(None),
                AdditionalFee.live_bid_min <= price,
                AdditionalFee.live_bid_max >= price
            )
            .order_by(AdditionalFee.live_bid_min)
            .limit(1)
        )
        return result.scalar_one_or_none()





