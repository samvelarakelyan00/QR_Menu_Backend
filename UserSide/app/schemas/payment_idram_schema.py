from pydantic import BaseModel, Field, condecimal
from typing import Optional


class PaymentIDramInitiationSchemaUserBasicTip(BaseModel):
    EDP_LANGUAGE: str = Field(..., description="Language for Idram interface")
    EDP_REC_ACCOUNT: str = Field(..., description="Idram ID of the merchant")
    EDP_DESCRIPTION: str = Field(..., description="Description of the product or service")
    EDP_AMOUNT: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(..., description="Amount of the payment")
    # EDP_BILL_NO: str = Field(..., description="Bill ID according to merchant's accounting system")
    EDP_EMAIL: Optional[str] = Field(None, description="Email address for payment confirmation notifications")
    REQUIRED_PAYMENT_AMOUNT: condecimal(gt=99, lt=100001, max_digits=5, decimal_places=2) = Field(..., description="Required payment amount")
    HoReKaClientId: int


class PaymentIDramStatusSchemaUserBasicTip:
    PENDING: str = "pending"
    PAID: str = "paid"
    FAIL: str = "failed"


class PaymentIDramStatusUpdateSchemaUserBasicTip(BaseModel):
    order_id: int = Field(..., description="Order ID of the payment")
    status: str = Field(..., description="New status of the payment")


class StartPaymentIDramResponseSchemaUserBasicTip(BaseModel):
    payment_url: str
    order_id: int
    status: str
    required_payment_amount: float = 100.00


class PaymentIDramResultSchemaUserBasicTip(BaseModel):
    EDP_PRECHECK: str = Field(..., description="Indicates if the request is preliminary")
    EDP_BILL_NO: int = Field(..., description="Bill number from the merchant's accounting system")
    EDP_REC_ACCOUNT: str = Field(..., description="IdramID of the merchant")
    EDP_PAYER_ACCOUNT: str = Field(..., description="IdramID of the customer")
    EDP_AMOUNT: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(..., description="Amount of the payment")
    EDP_TRANS_ID: str = Field(..., description="Transaction ID from Idram system")
    EDP_TRANS_DATE: str = Field(..., description="Transaction date from Idram system in dd/mm/yyyy format")
    EDP_SIGNATURE: str = Field(..., description="Signature for verifying request authenticity")

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "EDP_PRECHECK": "YES",
    #             "EDP_BILL_NO": "123456",
    #             "EDP_REC_ACCOUNT": "100000114",
    #             "EDP_PAYER_ACCOUNT": "200000256",
    #             "EDP_AMOUNT": "4800.00",
    #             "EDP_TRANS_ID": "20210915000123",
    #             "EDP_TRANS_DATE": "15/09/2021",
    #             "EDP_SIGNATURE": "abc123def456"
    #         }
    #     }
