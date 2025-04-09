from pydantic import BaseModel, ConfigDict


class TableCreate(BaseModel):
    name: str
    seats: int
    location: str


class TableOut(TableCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
