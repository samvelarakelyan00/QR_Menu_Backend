# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.horeka_admin_schema import (
    HoReKaClientAdminCreateSchema
)

from services import admin_auth as admin_auth_service
from services import horekaAdminCRUD as horekaAdminCRUD_service


router = APIRouter(
    prefix='/horekaAdminCRUD',
    tags=["HoReKa Admin CRUD"]
)


@router.post("/add-new-horeka-client-admin")
def login(horeka_client_admin_create_data: HoReKaClientAdminCreateSchema,
          service: horekaAdminCRUD_service.HoReKaAdminCRUDService = Depends(),
          current_admin=Depends(admin_auth_service.get_current_admin)):

    return service.create_horeka_client_admin(horeka_client_admin_create_data)
