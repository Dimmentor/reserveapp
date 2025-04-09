from pydantic import BaseModel, ConfigDict


class TableCreate(BaseModel):
    table_number: int
    capacity: int

class TableOut(TableCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)