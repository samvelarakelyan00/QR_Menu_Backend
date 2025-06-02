import datetime

# FastAPI
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status, Request
from fastapi.responses import ORJSONResponse
#
# # Own
# # from schemas.auth_schemas import (
# #     UserCreate,
# #     Token,
# #     LoginForm
# # )
#
# # from schemas.user_schemas import (
# #     ResetPasswordSchema,
# #     PasswordChangeSchema,
# #     UsernameChangeSchema,
# #     CurrentFreeSipSchema,
# #     UserOutSchema,
# # )
#

from schemas.auth_schema import (
    CafeAdminOut
)
from schemas.payment_idram_schema import (
    PaymentIDramInitiationSchemaSubsPlan,
    PaymentIDramStatusSchema,
    PaymentIDramStatusUpdateSchema,
    StartPaymentIDramResponseSchemaHoReKaSubsPlan,
    PaymentIDramResultSchema
)

from services.PaymentIDram import horeca_subs_payment_check as horeca_subs_idram_payment_check_service
from services import admin_auth as cafe_admin_auth_service


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


router = APIRouter(
    prefix='/payment/idram',
    tags=["HoReCa Subs Plan IDram Payment Check"]
)


@router.get("/find-horeca_admin-by-id", response_model=CafeAdminOut)
def find_user_by_username(
    payment_service: horeca_subs_idram_payment_check_service.CheckHoReCaSubsPlanService = Depends(),
    current_admin = Depends(cafe_admin_auth_service.get_current_admin)
):
    horeca_admin_id = current_admin.__dict__.get("id")

    return payment_service.find_horeka_admin(horeca_admin_id)


# # @router.get('/required-payment-amount')
# # def get_required_payment_amount(
# #     payment_service: payment_service.PaymentService = Depends(),
# #     current_user=Depends(auth_service.get_current_user)
# # ):
# #     user_id = current_user.__dict__.get("user_id")
# #
# #     return payment_service.get_required_payment_amount(user_id)


# # @router.get('/user-last-payment')
# # def get_user_last_payment(payment_service: payment_service.PaymentService = Depends(),
# #                           current_user=Depends(auth_service.get_current_user)):
# #     user_id = current_user.__dict__.get("user_id")
# #
# #     return payment_service.get_user_last_payment(user_id)
# #
# #
# # @router.get('/check-user-payment')
# # def check_user_payment(payment_service: payment_service.PaymentService = Depends(),
# #                           current_user=Depends(auth_service.get_current_user)):
# #     user_id = current_user.__dict__.get("user_id")
# #
# #     return payment_service.check_user_payment(user_id)
# #
# #
# # @router.get('/get-payment-amount-by-subs-plan')
# # def get_payment_amount_by_subs_plan(payment_service: payment_service.PaymentService = Depends(),
# #                           current_user=Depends(auth_service.get_current_user)):
# #
# #     return payment_service.get_payment_amount_by_subs_plan()
