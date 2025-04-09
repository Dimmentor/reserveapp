from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReservationCreate(BaseModel):
    table_id: int
    start_time: datetime
    end_time: datetime

class ReservationOut(ReservationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)