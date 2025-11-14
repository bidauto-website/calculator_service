from pydantic import BaseModel, Field

from app.core.utils import create_pagination_page
from app.database.schemas.location import LocationRead
from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum
from app.enums.vehicle_type import VehicleTypeEnum


class CalculatorDataIn(BaseModel):
    price: int = Field(..., gt=0, description="Price for vehicle")
    auction: AuctionEnum = Field(..., description="Auction")
    fee_type: FeeTypeEnum | None = Field(description="Fee type", default=FeeTypeEnum.NON_CLEAN_TITLE_FEE)
    vehicle_type: VehicleTypeEnum = Field(...,description="Vehicle type")
    destination: str | None = Field(None, description="Destination (Port in Europe)")
    location: str = Field(..., description="Location")

class CalculatorWithoutDetailsIn(BaseModel):
    price: int = Field(..., gt=0, description="Price for vehicle")
    destination: str | None = Field(None, description="Destination (Port in Europe)")


class GetLocationsIn(BaseModel):
    search: str | None = Field(None, description="Search by location name")
    auction: AuctionEnum | None = Field(None, description="Auction")

LocationPage = create_pagination_page(LocationRead)

