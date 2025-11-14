from pydantic import BaseModel, ConfigDict

class ExchangeRateCreate(BaseModel):
    rate: float

class ExchangeRateUpdate(BaseModel):
    rate: float | None = None

class ExchangeRateRead(ExchangeRateCreate):
    id: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)
