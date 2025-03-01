from typing import Optional

from pydantic import BaseModel


class MenuAddNew(BaseModel):
    kind: str
    category: str
    name: str
    quantity: str
    price: float
    description: str
    language: str
    image_src: Optional[None | str] = None
    preparation_time: Optional[None | float] = None
    weight: Optional[None | float] = None
    calories: Optional[None | float] = None


class ProductUpdate(BaseModel):
    kind: Optional[None | str] = None
    category: Optional[None | str] = None
    name: Optional[None | str] = None
    quantity: Optional[None | str] = None
    price: Optional[None | float] = None
    description: Optional[None | str] = None
    image_src: Optional[None | str] = None
    preparation_time: Optional[None | float] = None
    weight: Optional[None | float] = None
    calories: Optional[None | float] = None
