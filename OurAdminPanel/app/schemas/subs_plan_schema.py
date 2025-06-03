from typing import Optional
from pydantic import BaseModel


class HoReCaSubsPlanCreateSchema(BaseModel):
    name: str
    amount: float
    duration: Optional[int] = 31


class HoReCaSubsPlanUpdateSchema(BaseModel):
    amount: Optional[None | float] = None
    duration: Optional[None | int] = None
