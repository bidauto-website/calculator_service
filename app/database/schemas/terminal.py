from pydantic import BaseModel, ConfigDict, Field



class TerminalCreate(BaseModel):
    name: str

class TerminalUpdate(BaseModel):
    name: str | None = Field(None)


class TerminalRead(TerminalCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
