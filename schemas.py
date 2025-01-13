from pydantic import BaseModel


class UserSignupSchema(BaseModel):
    username: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UsernameChangeSchema(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

