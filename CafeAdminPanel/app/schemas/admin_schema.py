from pydantic import BaseModel


class HoReKaAdminOutSchema(BaseModel):
    id: int
    horekaclient_id: int
    name: str
    email: str
