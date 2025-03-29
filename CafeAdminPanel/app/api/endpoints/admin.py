# FastAPI
import datetime

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
from schemas.admin_schema import (
    HoReKaAdminOutSchema
)

from services import admin_auth as cafe_admin_auth_service
from services import admin as admin_service
from services import payment_idram as payment_idram_service


router = APIRouter(
    prefix='/admin',
    tags=["Admin Operations"]
)


@router.get("", response_model=HoReKaAdminOutSchema)
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


@router.get("/my-account-page-info")
def get_horeka_admin_my_account_page_info(
    admin_servie=Depends(admin_service.AdminService),
    payment_idram_service=Depends(payment_idram_service.IDramPaymentService),
    current_admin=Depends(cafe_admin_auth_service.get_current_admin)
):
    try:
        horeka_admin_id = current_admin.__dict__.get("id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    horeka_admin_last_payment = payment_idram_service.get_horeka_admin_last_payment(horeka_admin_id)
    horeka_admin_page_info = admin_servie.get_horeka_admin_my_account_page_info(horeka_admin_id)

    if (horeka_admin_last_payment is None or
        horeka_admin_last_payment.__dict__.get("available_to") < datetime.datetime.now() + datetime.timedelta(hours=4)):

        horeka_admin_page_info.update(
            {
                "horeka_subs_plan": None,
                "horeka_subs_plan_expires": None
            }
        )
    else:
        horeka_admin_last_payment = horeka_admin_last_payment.__dict__
        horeka_subs_plan = horeka_admin_last_payment.get("subs_plan")
        horeka_subs_plan_expires = horeka_admin_last_payment.get("available_to")
        horeka_admin_page_info.update(
            {
                "horeka_subs_plan": horeka_subs_plan,
                "horeka_subs_plan_expires": horeka_subs_plan_expires
            }
        )

    return horeka_admin_page_info
