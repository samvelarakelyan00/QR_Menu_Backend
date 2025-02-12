from pydantic import BaseModel, EmailStr


class HoReKaClientAdminCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    horekaclient_id: int
