# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
# from schemas.menu_schema import (
#     MenuAddNew
# )

from services import admin_auth as cafe_admin_auth_service
from services import admin as admin_service


router = APIRouter(
    prefix='/admin',
    tags=["Admin Operations"]
)


@router.get("")
def get_menu_by_product_id(
    admin_servie=Depends(admin_service.AdminService),
    current_admin=Depends(cafe_admin_auth_service.get_current_admin)
):

    try:
        horeka_admin_id = current_admin.__dict__.get("id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return admin_servie.get_horeka_admin_by_id(horeka_admin_id)
