from pydantic import BaseModel, ConfigDict, Field

from app.enums.auction import AuctionEnum, SpecificAuctionEnum
from app.enums.vehicle_type import VehicleTypeEnum


class VehicleTypeCreate(BaseModel):
    auction: AuctionEnum
    vehicle_type: VehicleTypeEnum
    specific_type: SpecificAuctionEnum | None = None

class VehicleTypeUpdate(BaseModel):
    auction: AuctionEnum | None = None
    vehicle_type: VehicleTypeEnum | None = None
    specific_type: SpecificAuctionEnum | None = None

class VehicleTypeRead(BaseModel):
    id: int
    city_id: int
    vehicle_type: VehicleTypeEnum
    fee_amount: int
    is_default: bool

    model_config = ConfigDict(from_attributes=True)
