import os

# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from services import user as user_service
from services import horeka_reservation as reservation_service

from schemas.horeka_reservations_schemas import (
    ReservationCreateSchema
)

router = APIRouter(
    prefix='/cafe/reservations',
    tags=["Reservations"]
)


@router.post("/{horeka_id}")
def make_reservation(horeka_id:  int,
                     reservation_data: ReservationCreateSchema,
                     reservation_service=Depends(reservation_service.ReservationService)
                     ):
    return reservation_service.make_reservation(reservation_data, horeka_id=horeka_id)
