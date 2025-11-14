from pydantic import BaseModel, ConfigDict, Field



class LocationCreate(BaseModel):
    name: str
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    email: str | None = None


class LocationUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    email: str | None = None

class LocationRead(LocationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
