from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models

from schemas.horeka_reservations_schemas import (
    ReservationCreateSchema
)


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class ReservationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def make_reservation(self, reservation_data: ReservationCreateSchema, horeka_id: int):
        try:
            reservation = models.Reservation(**dict(reservation_data), horeka_client_id=horeka_id)
            self.session.add(reservation)
            self.session.commit()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        return "OK"
