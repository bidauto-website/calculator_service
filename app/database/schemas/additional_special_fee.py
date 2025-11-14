from pydantic import BaseModel, ConfigDict

from app.enums.auction import AuctionEnum
from app.enums.vehicle_type import VehicleTypeEnum


class AdditionalSpecialFeeCreate(BaseModel):
    name: str
    auction: AuctionEnum
    amount: int


class AdditionalSpecialFeeUpdate(BaseModel):
    name: str | None
    auction: VehicleTypeEnum | None
    amount: int | None

class AdditionalSpecialFeeRead(AdditionalSpecialFeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
