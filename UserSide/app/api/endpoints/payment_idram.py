import datetime

# FastAPI
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status, Request
from fastapi.responses import ORJSONResponse

# Own
# from schemas.auth_schemas import (
#     UserCreate,
#     Token,
#     LoginForm
# )

# from schemas.user_schemas import (
#     ResetPasswordSchema,
#     PasswordChangeSchema,
#     UsernameChangeSchema,
#     CurrentFreeSipSchema,
#     UserOutSchema,
# )

from schemas.payment_idram_schema import (
    PaymentIDramInitiationSchemaUserBasicTip,
    PaymentIDramStatusSchemaUserBasicTip,
    PaymentIDramStatusUpdateSchemaUserBasicTip,
    StartPaymentIDramResponseSchemaUserBasicTip,
    PaymentIDramResultSchemaUserBasicTip
)

from services import payment_idram as idram_payment_service


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


router = APIRouter(
    prefix='/payment/idram/users/basic-tip',
    tags=["Payment IDram User Basic Tip"]
)


# @router.get("/find-user-by-user-id/{user_id}")
# def find_user_by_username(
#     user_id: int,
#     payment_service: payment_service.PaymentService = Depends(),
#     current_user = Depends(auth_service.get_current_user)
# ):
#     return payment_service.find_user(user_id)
#
#
# @router.get('/required-payment-amount')
# def get_required_payment_amount(
#     payment_service: payment_service.PaymentService = Depends(),
#     current_user=Depends(auth_service.get_current_user)
# ):
#     user_id = current_user.__dict__.get("user_id")
#
#     return payment_service.get_required_payment_amount(user_id)

@router.post("/start-payment")  # response_model=StartPaymentResponseSchema
def start_payment(payment_data: PaymentIDramInitiationSchemaUserBasicTip,
                    payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends(),
                    ):

    return payment_service.start_payment(payment_data)


@router.get("/payment-success")
def payment_success(order_id: str,
                    payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends(),
                    ):  # data: PaymentStatusUpdateSchema,

    return payment_service.payment_success(order_id)


@router.get("/payment-fail")
def payment_fail(order_id: str,
                    payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends(),
                    ):  # data: PaymentStatusUpdateSchema,

    return payment_service.payment_fail(order_id)


@router.post("/payment-result")
def payment_result(
        EDP_PRECHECK: str = Form(None),  # Allow None for the pre-check
        EDP_BILL_NO: str = Form(...),
        EDP_REC_ACCOUNT: str = Form(...),
        EDP_PAYER_ACCOUNT: str = Form(None),  # Payer account only for confirmation
        EDP_AMOUNT: float = Form(...),
        EDP_TRANS_ID: str = Form(None),  # Transaction ID only for confirmation
        EDP_TRANS_DATE: str = Form(None),  # Transaction date only for confirmation
        EDP_SIGNATURE: str = Form(None),  # Signature only for confirmation
        payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends()
):

    return payment_service.payment_result(
        EDP_PRECHECK,
        EDP_BILL_NO,
        EDP_REC_ACCOUNT,
        EDP_PAYER_ACCOUNT,
        EDP_AMOUNT,
        EDP_TRANS_ID,
        EDP_TRANS_DATE,
        EDP_SIGNATURE,
    )


# @router.get('/user-last-payment')
# def get_user_last_payment(payment_service: payment_service.PaymentService = Depends(),
#                           current_user=Depends(auth_service.get_current_user)):
#     user_id = current_user.__dict__.get("user_id")
#
#     return payment_service.get_user_last_payment(user_id)
#
#
# @router.get('/check-user-payment')
# def check_user_payment(payment_service: payment_service.PaymentService = Depends(),
#                           current_user=Depends(auth_service.get_current_user)):
#     user_id = current_user.__dict__.get("user_id")
#
#     return payment_service.check_user_payment(user_id)
#
#
# @router.get('/get-payment-amount-by-subs-plan')
# def get_payment_amount_by_subs_plan(payment_service: payment_service.PaymentService = Depends(),
#                           current_user=Depends(auth_service.get_current_user)):
#
#     return payment_service.get_payment_amount_by_subs_plan()
