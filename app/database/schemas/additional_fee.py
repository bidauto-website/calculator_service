from pydantic import BaseModel, ConfigDict, Field


class AdditionalFeeCreate(BaseModel):
    int_proxy_min: float | None = Field(None)
    int_proxy_max: float | None = Field(None)
    int_fee: float | None = Field(None)
    proxy_fee: float | None = Field(None)
    live_bid_min: float | None = Field(None)
    live_bid_max: float | None = Field(None)
    live_bid_fee: float | None = Field(None)


class AdditionalFeeUpdate(AdditionalFeeCreate):
    pass

class AdditionalFeeRead(AdditionalFeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
