from pydantic import BaseModel, Field

from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum
from app.enums.vehicle_type import VehicleTypeEnum


class CalculatorDataIn(BaseModel):
    price: int = Field(..., gt=-1, description="Price for vehicle")
    auction: AuctionEnum = Field(..., description="Auction")
    fee_type: FeeTypeEnum | None = Field(description="Fee type", default=FeeTypeEnum.NON_CLEAN_TITLE_FEE)
    vehicle_type: VehicleTypeEnum = Field(..., description="Vehicle type")
    destination: str | None = Field(None, description="Destination (Port in Europe)")
    location: str = Field(..., description="Location")


class PriceIn(BaseModel):
    price: int = Field(..., gt=0, description="Price for vehicle")

