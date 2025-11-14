from pydantic import BaseModel, ConfigDict

class FeeCreate(BaseModel):
    car_price_min: int
    car_price_max: int
    car_price_fee: int

class FeeUpdate(BaseModel):
    car_price_min: int | None
    car_price_max: int | None
    car_price_fee: int | None

class FeeRead(FeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
