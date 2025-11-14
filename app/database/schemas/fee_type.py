from pydantic import BaseModel, ConfigDict

from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum


class FeeTypeCreate(BaseModel):
    auction: AuctionEnum
    fee_type: FeeTypeEnum

class FeeTypeUpdate(BaseModel):
    auction: AuctionEnum | None
    fee_type: FeeTypeEnum | None

class FeeTypeRead(FeeTypeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
