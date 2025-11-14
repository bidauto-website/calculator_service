from pydantic import BaseModel, ConfigDict

class DeliveryPriceCreate(BaseModel):
   price: int
   vehicle_type_id: int

class DeliveryPriceUpdate(BaseModel):
    price: int | None = None

class DeliveryPriceRead(DeliveryPriceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
