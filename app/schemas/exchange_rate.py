from pydantic import Field, BaseModel


class ExchangeRateIn(BaseModel):
    rate: float = Field(..., gt=0)