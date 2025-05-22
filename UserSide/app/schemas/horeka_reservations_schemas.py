import datetime

from typing import Optional
from pydantic import BaseModel, EmailStr


class ReservationCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    reserve_date: datetime.date
    reserve_time: datetime.time
    guests_count: int = 1
    special_requests: Optional[None | str] = None
