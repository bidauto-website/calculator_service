from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import VehicleType

from app.database.schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate
from app.enums.auction import AuctionEnum
from app.enums.vehicle_type import VehicleTypeEnum


class VehicleTypeService(BaseService[VehicleType, VehicleTypeCreate, VehicleTypeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(VehicleType, session)

    async def get_by_auction_and_type(self, auction: AuctionEnum, vehicle_type: VehicleTypeEnum) -> VehicleType | None:
        result = await self.session.execute(select(VehicleType).where(VehicleType.auction == auction, VehicleType.vehicle_type == vehicle_type))
        return result.scalar_one_or_none()





