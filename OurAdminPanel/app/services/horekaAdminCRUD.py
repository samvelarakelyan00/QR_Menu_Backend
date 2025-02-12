from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy.orm.session import Session


# Own
from database import get_session
from models import models
import security


from schemas.horeka_admin_schema import (
    HoReKaClientAdminCreateSchema
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class HoReKaAdminCRUDService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_horeka_client_admin(self, horeka_client_admin_create_data: HoReKaClientAdminCreateSchema):
        try:
            horeka_client_admin_create_data.password = security.hash_password(horeka_client_admin_create_data.password)
        except Exception  as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err
            )

        try:
            new_horeka_client_admin = models.HoReKaAdmin(**horeka_client_admin_create_data.dict())

            self.session.add(new_horeka_client_admin)
            self.session.commit()

            return "OK"
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err
            )
