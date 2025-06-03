# FastAPI
import datetime

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
from schemas.subs_plan_schema import (
    HoReCaSubsPlanCreateSchema,
    HoReCaSubsPlanUpdateSchema
)

from services import admin_auth as admin_auth_service
from services import subs_plan_crud as subs_plan_crud_service


router = APIRouter(
    prefix='/subs-plan',
    tags=["HoReCa Subscriptions CRUD"]
)


@router.post("/add")
def get_menu_by_product_id(
    subs_plan_data: HoReCaSubsPlanCreateSchema,
    admin_servie=Depends(subs_plan_crud_service.HoReCaSubsPlanCRUD),
    current_admin=Depends(admin_auth_service.get_current_admin)
):

    return admin_servie.add_new_horeca_subs_plan(subs_plan_data)

@router.get("/all")
def get_available_subs_plans(
    admin_servie=Depends(subs_plan_crud_service.HoReCaSubsPlanCRUD),
    current_admin=Depends(admin_auth_service.get_current_admin)
):

    return admin_servie.get_available_subs_plans()


@router.get("/by-name/{name}")
def get_subs_plan_by_name(
    name: str,
    admin_servie=Depends(subs_plan_crud_service.HoReCaSubsPlanCRUD),
    current_admin=Depends(admin_auth_service.get_current_admin)
):

    return admin_servie.get_subs_plan_by_name(name)


@router.put("/update/{subs_plan_id}")
def update_subs_plan(
    subs_plan_id: int,
    subs_plan_update_data: HoReCaSubsPlanUpdateSchema,
    admin_servie=Depends(subs_plan_crud_service.HoReCaSubsPlanCRUD),
    current_admin=Depends(admin_auth_service.get_current_admin)
):

    return admin_servie.update_subs_plan(subs_plan_id, subs_plan_update_data)


@router.delete("/delete/{subs_plan_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_subs_plan(
    subs_plan_id: int,
    admin_servie=Depends(subs_plan_crud_service.HoReCaSubsPlanCRUD),
    current_admin=Depends(admin_auth_service.get_current_admin)
):

    return admin_servie.delete_subs_plan(subs_plan_id)
