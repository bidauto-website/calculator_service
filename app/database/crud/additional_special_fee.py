from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.additional_special_fee import AdditionalSpecialFee


from app.database.schemas.additional_special_fee import AdditionalSpecialFeeCreate, AdditionalSpecialFeeUpdate
from app.enums.auction import AuctionEnum


class AdditionalSpecialFeeService(BaseService[AdditionalSpecialFee, AdditionalSpecialFeeCreate, AdditionalSpecialFeeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(AdditionalSpecialFee, session)

    async def get_additional_special_fee(self, auction: AuctionEnum)-> Sequence[AdditionalSpecialFee]:
        result = await self.session.execute(
            select(AdditionalSpecialFee).where(
                AdditionalSpecialFee.auction == auction
            )
        )
        return result.scalars().all()




