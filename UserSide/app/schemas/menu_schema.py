from typing import Optional

from pydantic import BaseModel


class HoReKaClientResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    image_src: str
    logo: str
