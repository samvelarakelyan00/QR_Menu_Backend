import hashlib

from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi import status, Depends, Form

# SqlAlchemy
from sqlalchemy import func
from sqlalchemy.orm.session import Session

# Own
from schemas.payment_idram_schema import (
    PaymentIDramInitiationSchemaSubsPlan,
    PaymentIDramStatusSchema,
    PaymentIDramStatusUpdateSchema,
    StartPaymentIDramResponseSchemaHoReKaSubsPlan,
    PaymentIDramResultSchema
)

from database import get_session
from models import models


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}

SECRET_KEY = "secret1234"


class IDramPaymentServiceHoReKaSubsPlan:
    @staticmethod
    def payment_success():
        return FileResponse("./templates/success.html")

    @staticmethod
    def payment_fail():
        return FileResponse("./templates/fail.html")

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_next_order_id(self):
        max_order_id = self.session.query(func.max(models.Payment.order_id)).scalar()
        if max_order_id is None:
            return 1
        return int(max_order_id) + 1

    def start_payment(self, horeka_client_id: int, payment_data: PaymentIDramInitiationSchemaSubsPlan):
        try:
            amount = payment_data.EDP_AMOUNT
            required_payment_amount = payment_data.REQUIRED_PAYMENT_AMOUNT
            subs_plan = payment_data.EDP_SUBS_PLAN
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if amount != required_payment_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Incorrect amount"
            )

        try:
            next_order_id = str(self.get_next_order_id())
            print(next_order_id)
            payment_status = "pending"

            payment = models.Payment(
                order_id=next_order_id,
                amount=amount,
                status=payment_status,
                horeka_client_id=horeka_client_id,
                subs_plan=subs_plan
            )

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

        try:
            self.session.add(payment)
            self.session.commit()
            self.session.refresh(payment)
        except Exception as err:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
        finally:
            self.session.close()

        data_to_sign = f"{payment_data.EDP_REC_ACCOUNT}:{payment_data.EDP_AMOUNT}:{next_order_id}:{SECRET_KEY}"
        signature = hashlib.sha256(data_to_sign.encode('utf-8')).hexdigest()

        payment_url = (
            "https://banking.idram.am/Payment/GetPayment?"
            f"EDP_LANGUAGE={payment_data.EDP_LANGUAGE}&"
            f"EDP_REC_ACCOUNT={payment_data.EDP_REC_ACCOUNT}&"
            f"EDP_DESCRIPTION={payment_data.EDP_DESCRIPTION}&"
            f"EDP_AMOUNT={payment_data.EDP_AMOUNT}&"
            f"EDP_BILL_NO={next_order_id}&"
            f"EDP_EMAIL={payment_data.EDP_EMAIL or ''}&"
            f"EDP_SIGNATURE={signature}"
        )

        return StartPaymentIDramResponseSchemaHoReKaSubsPlan(
            payment_url=payment_url,
            order_id=payment.order_id,
            status="pending",
            required_payment_amount=required_payment_amount
        )

    def payment_result(self,
                       EDP_PRECHECK: str = Form(None),
                       EDP_BILL_NO: str = Form(...),
                       EDP_REC_ACCOUNT: str = Form(...),
                       EDP_PAYER_ACCOUNT: str = Form(None),
                       EDP_AMOUNT: float = Form(...),
                       EDP_TRANS_ID: str = Form(None),
                       EDP_TRANS_DATE: str = Form(None),
                       EDP_CHECKSUM: str = Form(None),
                       EDP_SIGNATURE: str = Form(None)):

        if EDP_PRECHECK == "YES":
            try:
                payment = self.session.query(models.Payment).filter(models.Payment.order_id == str(EDP_BILL_NO)).first()
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if payment is None or round(payment.amount, 2) != round(EDP_AMOUNT, 2):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Order not found or amount mismatch")

            return PlainTextResponse(content="OK", status_code=200)
        else:
            try:
                payment = self.session.query(models.Payment).filter(models.Payment.order_id == str(EDP_BILL_NO)).first()
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if payment is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            # # TODO check given data for CHECK_SUM validation
            # # Validate required fields for payment confirmation
            # if not (EDP_PAYER_ACCOUNT and EDP_BILL_NO and EDP_REC_ACCOUNT and EDP_AMOUNT and EDP_TRANS_ID and EDP_TRANS_DATE and EDP_CHECKSUM):
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Missing required fields for signature validation"
            #     )
            #
            # # TODO if given CHECK_SUM != expected CHECK_SUM -> fail
            # # Validate the signature (MD5)
            # try:
            #     # Create the string to hash
            #     txt_to_hash = f"{EDP_REC_ACCOUNT}:{EDP_AMOUNT}:{SECRET_KEY}:{EDP_BILL_NO}:{EDP_PAYER_ACCOUNT}:{EDP_TRANS_ID}:{EDP_TRANS_DATE}"
            #
            #     # Generate the expected checksum using MD5
            #     expected_checksum = hashlib.md5(txt_to_hash.encode('utf-8')).hexdigest().upper()
            #
            #     # Compare the received checksum with the expected checksum
            #     if EDP_CHECKSUM.upper() != expected_checksum:
            #         print(f"Invalid checksum for Bill No: {EDP_BILL_NO}")
            #         try:
            #             payment.status = "failed"
            #             self.session.commit()
            #         except Exception as err:
            #             raise HTTPException(
            #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #                 detail="Error while trying to set payment status as 'failed'\n"
            #                        f"ERR: {err}"
            #             )
            #         raise HTTPException(
            #             status_code=status.HTTP_400_BAD_REQUEST,
            #             detail="Invalid checksum"
            #         )
            # except Exception as err:
            #     raise HTTPException(
            #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #         detail="Error occurred while validating checksum\n"
            #                f"ERR: {err}"
            #     )

            try:
                payment.status = "paid"
                payment.trans_id = EDP_TRANS_ID
                payment.trans_date = EDP_TRANS_DATE
                payment.payer_account = EDP_PAYER_ACCOUNT

                self.session.commit()
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return PlainTextResponse(content="OK", status_code=200)
