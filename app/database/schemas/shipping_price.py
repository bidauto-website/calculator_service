from pydantic import BaseModel, ConfigDict, Field



class ShippingPriceCreate(BaseModel):
    price: int


class ShippingPriceUpdate(BaseModel):
    price: int | None = Field(None)

class ShippingPriceRead(ShippingPriceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
