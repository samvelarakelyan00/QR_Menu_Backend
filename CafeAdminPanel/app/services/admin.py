from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic.v1 import NoneIsAllowedError

# SqlAlchemy
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class AdminService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_horeka_admin_by_id(self, admin_id: int):
        try:
            horeka_admin = self.session.query(models.HoReKaAdmin).filter_by(id=admin_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if horeka_admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"HoReKa admin with id '{admin_id}' was not found!"
            )

        return horeka_admin
