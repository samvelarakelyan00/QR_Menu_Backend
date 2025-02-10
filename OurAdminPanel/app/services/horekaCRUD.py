from fastapi import Depends

# SqlAlchemy
from sqlalchemy.orm.session import Session


# Own
from database import get_session


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class HoReKaCRUDService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
