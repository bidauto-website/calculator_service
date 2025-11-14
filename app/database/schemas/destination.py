from pydantic import BaseModel, ConfigDict


class DestinationCreate(BaseModel):
    name: str

class DestinationUpdate(BaseModel):
    name: str | None

class DestinationRead(DestinationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
