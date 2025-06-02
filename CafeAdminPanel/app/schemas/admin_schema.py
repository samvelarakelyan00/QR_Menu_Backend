from pydantic import BaseModel
from typing import Optional


class HoReKaAdminOutSchema(BaseModel):
    id: int
    horekaclient_id: int
    name: str
    email: str


class HoReCaSubsPlanCreateSchema(BaseModel):
    name: str
    amount: float
    duration: Optional[int] = 31


class HoReCaSubsPlanUpdateSchema(BaseModel):
    amount: Optional[None | float] = None
    duration: Optional[None | int] = None
