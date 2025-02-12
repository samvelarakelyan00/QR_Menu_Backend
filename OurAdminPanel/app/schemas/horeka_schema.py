from pydantic import BaseModel, EmailStr


class HoReKaClientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    class Config:
        from_attributes = True
