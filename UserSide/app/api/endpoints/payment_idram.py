# FastAPI
from fastapi import APIRouter, Depends, Form

# Own
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
    tags=["PaymentIDram IDram User Basic Tip"]
)


@router.post("/start-payment")
def start_payment(payment_data: PaymentIDramInitiationSchemaUserBasicTip,
                    payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends(),
                    ):

    return payment_service.start_payment(payment_data)


@router.get("/payment-success")
def payment_success(payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends()):

    return payment_service.payment_success()


@router.get("/payment-fail")
def payment_fail(payment_service: idram_payment_service.IDramPaymentServiceUserBasicTip = Depends()):

    return payment_service.payment_fail()


@router.post("/payment-result")
def payment_result(
        EDP_PRECHECK: str = Form(None),
        EDP_BILL_NO: str = Form(...),
        EDP_REC_ACCOUNT: str = Form(...),
        EDP_PAYER_ACCOUNT: str = Form(None),
        EDP_AMOUNT: float = Form(...),
        EDP_TRANS_ID: str = Form(None),
        EDP_TRANS_DATE: str = Form(None),
        EDP_SIGNATURE: str = Form(None),
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
