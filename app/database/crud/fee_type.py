from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import FeeType


from app.database.schemas.fee_type import FeeTypeUpdate, FeeTypeCreate
from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum


class FeeTypeService(BaseService[FeeType, FeeTypeCreate, FeeTypeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(FeeType, session)

    async def get_by_fee_auction(self, auction: AuctionEnum, fee_type: FeeTypeEnum) -> FeeType | None:
        result = await self.session.execute(
            select(FeeType).where(
                FeeType.auction == auction,
                FeeType.fee_type == fee_type
            )
        )
        return result.scalar_one_or_none()



