# FastAPI
from fastapi import APIRouter, Depends, Form

# My modules
from schemas.payment_idram_schema import (
    PaymentIDramInitiationSchemaSubsPlan,
    PaymentIDramStatusSchema,
    PaymentIDramStatusUpdateSchema,
    StartPaymentIDramResponseSchemaHoReKaSubsPlan,
    PaymentIDramResultSchema
)

from services.PaymentIDram import payment_idram as idram_payment_service
from services.Admin import admin_auth as cafe_admin_auth_service


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


router = APIRouter(
    prefix='/payment/idram',
    tags=["Payment IDram"]
)


@router.post("/start-payment")  # response_model=StartPaymentResponseSchema
def start_payment(payment_data: PaymentIDramInitiationSchemaSubsPlan,
                  payment_service: idram_payment_service.IDramPaymentServiceHoReKaSubsPlan = Depends(),
                  current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    horeka_client_id = current_admin.__dict__.get("horekaclient_id")

    return payment_service.start_payment(horeka_client_id, payment_data)


@router.get("/payment-success")
def payment_success(payment_service: idram_payment_service.IDramPaymentServiceHoReKaSubsPlan = Depends()):

    return payment_service.payment_success()


@router.get("/payment-fail")
def payment_fail(payment_service: idram_payment_service.IDramPaymentServiceHoReKaSubsPlan = Depends()):

    return payment_service.payment_fail()


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
        payment_service: idram_payment_service.IDramPaymentServiceHoReKaSubsPlan = Depends()
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
