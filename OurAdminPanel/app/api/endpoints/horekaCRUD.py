# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.horeka_schema import (
    HoReKaClientCreateSchema
)

from services import admin_auth as admin_auth_service
from services import horekaCRUD as horekaCRUD_service


router = APIRouter(
    prefix='/horekaCRUD',
    tags=["HoReKa CRUD"]
)


@router.post("/add-new-horeka-client")
def login(horeka_client_create_data: HoReKaClientCreateSchema,
          service: horekaCRUD_service.HoReKaCRUDService = Depends(),
          current_admin=Depends(admin_auth_service.get_current_admin)):

    return service.create_horeka_client(horeka_client_create_data)
