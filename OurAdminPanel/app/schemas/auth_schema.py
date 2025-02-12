from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseAdmin(BaseModel):
    name: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

    class Config:
        from_attributes = True


class AdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class AdminLoginForm(BaseModel):
    email: str
    password: str
