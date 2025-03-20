from pydantic import BaseModel, EmailStr


class HoReKaClientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    image_src: str
    logo: str
    payment_amount: float

    class Config:
        from_attributes = True
