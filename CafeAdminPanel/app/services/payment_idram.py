import hashlib
import datetime

from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi import status, Depends, Form

# SqlAlchemy
from sqlalchemy import desc, func
from sqlalchemy import and_
from sqlalchemy.orm.session import Session

# Own
from schemas.payment_idram_schema import (
    PaymentIDramInitiationSchema,
    PaymentIDramStatusSchema,
    PaymentIDramStatusUpdateSchema,
    StartPaymentIDramResponseSchema,
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

SECRET_KEY = "7saWDJZkFmaJ4elKoClpDJsi3w8gBUTdzDUKJ6"


class IDramPaymentService: # TODO
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def find_horeka_admin(self, horeka_admin_id: int):
        try:
            horeka_admin = self.session.query(models.HoReKaAdmin).filter(models.HoReKaAdmin.id == horeka_admin_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while trying to find horeka admin with id '{horeka_admin_id}'\n"
                       f"ERR: {err}"
            )

        if horeka_admin is None:
            self.session.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"HoReKa admin with id '{horeka_admin_id}' was not found!"
            )

        return horeka_admin

    def get_horeka_admin_last_payment(self, horeka_admin_id: int):
        try:
            horeka_admin = self.find_horeka_admin(horeka_admin_id)
            horeka_client_id = horeka_admin.__dict__.get("horekaclient_id")
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        try:
            last_payment = (self.session.query(models.Payment)
                            .filter(and_(models.Payment.horeka_client_id == horeka_client_id, models.Payment.status == 'paid'))
                            .order_by(desc(models.Payment.updated_at))
                            .first())
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        return last_payment
    #
    # def check_user_payment(self, user_id):
    #     try:
    #         usr = self.session.query(models.User).filter_by(user_id=user_id).first()
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=err
    #         )
    #
    #     if usr is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"User with id '{user_id}' was not found!"
    #         )
    #
    #     usr = usr.__dict__
    #
    #     try:
    #         is_user_free = self.session.query(models.FreeUsers).filter_by(email=usr.get('email')).first()
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=err
    #         )
    #
    #     if (not is_user_free is None and
    #             is_user_free.__dict__.get("end_date") >= datetime.datetime.now() + datetime.timedelta(hours=4)):
    #         return True
    #
    #     last_payment = self.get_user_last_payment(user_id)
    #     if last_payment is None:
    #         return False
    #
    #     last_payment = last_payment.__dict__
    #
    #     current_datetime = datetime.datetime.now() + datetime.timedelta(hours=4)
    #     payment_available_to = last_payment.get("available_to")
    #
    #     if payment_available_to < current_datetime:
    #         return False
    #
    #     return True
    #
    def get_next_order_id(self):
        # Query the maximum current order_id and increment by 1
        max_order_id = self.session.query(func.max(models.Payment.order_id)).scalar()
        return (max_order_id or 0) + 1
    #
    # def get_required_payment_amount(self, user_id):
    #     # Find Required payment amount
    #     try:
    #         user = self.session.query(models.User).filter_by(user_id=user_id).first()
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=err
    #         )
    #
    #     if user is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"User with id '{user_id}' was not found!"
    #         )
    #
    #     user = user.__dict__
    #     special_promocode = user.get("special_promocode")
    #
    #     try:
    #         partner = self.session.query(models.PartnerProgramSeller).filter_by(special_promo_code=special_promocode).first()
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=err
    #         )
    #
    #     if partner is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Partner with promo code '{special_promocode}' was not found!"
    #         )
    #
    #     partner = partner.__dict__
    #
    #     return {
    #         "promocode": partner.get("special_promo_code"),
    #         "price": partner.get("price")
    #     }
    #
    # def get_payment_amount_by_subs_plan(self):
    #     try:
    #         all_data = self.session.query(models.GoldnSipSubsPlans).all()
    #         return all_data
    #     except Exception as err:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                             detail=err)

    def start_payment(self, horeka_admin_id: int, payment_data: PaymentIDramInitiationSchema):
        try:
            amount = payment_data.EDP_AMOUNT
            required_payment_amount = payment_data.REQUIRED_PAYMENT_AMOUNT
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Can't get data\nERR: {err}"
            )

        if amount != required_payment_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Incorrect amount"
            )

        horeka_admin = self.find_horeka_admin(horeka_admin_id)
        # self.check_user_payment(user_id)  # Uncomment and ensure this function works as expected

        try:
            # Generate the next order_id
            next_order_id = self.get_next_order_id()

            # Correctly set the status as a string
            payment_status = "pending"  # Set the appropriate status string here

            # Create a new Payment instance
            payment = models.Payment(
                order_id=next_order_id,
                amount=amount,
                status=payment_status,  # Ensure this is a valid string
                horeka_client_id=dict(horeka_admin).get("horekaclient_id"),
                subs_plan=payment_data.EDP_SUBS_PLAN
            )
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while trying to make Payment model\nERR: {err}"
            )

        try:
            self.session.add(payment)
            self.session.commit()
            self.session.refresh(payment)
        except Exception as err:
            self.session.rollback()  # Ensure the session is rolled back on error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while trying to add payment data to db\nERR: {err}"
            )
        finally:
            self.session.close()  # Close the session in a finally block to ensure it's always executed

            # Generate signature using secret key
            # Generate signature using secret key
        data_to_sign = f"{payment_data.EDP_REC_ACCOUNT}:{payment_data.EDP_AMOUNT}:{next_order_id}:{SECRET_KEY}"
        signature = hashlib.sha256(data_to_sign.encode('utf-8')).hexdigest()

        # Construct the payment URL with necessary fields for Idram including the signature
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

        print(f"Payment URL: {payment_url}")  # Debug print to verify the URL construction
        print(payment_data.EDP_REC_ACCOUNT, "payment_data.EDP_REC_ACCOUNT")

        # Return the payment URL and status
        return StartPaymentIDramResponseSchema(
            payment_url=payment_url,
            order_id=payment.order_id,
            status="pending",
            required_payment_amount=required_payment_amount
        )

    def payment_success(self):  # payment_status_update_data: PaymentStatusUpdateSchema
        return FileResponse("../templates/success.html")

    def payment_fail(self):  # payment_status_update_data: PaymentStatusUpdateSchema
        return FileResponse("../templates/fail.html")

    # def payment_data_to_users_with_subs(self, edp_bill_no):
    #     # ============== Store needed data to users_with_subs ===============
    #     try:
    #         # Check if the order exists and the amount is correct
    #         payment = self.session.query(models.Payment).filter(models.Payment.order_id == int(edp_bill_no)).first()
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Error occurred while trying to find the payment with EDP_BILL_NO '{edp_bill_no}'\n"
    #                    f"Check if the order exists and the amount is correct\n"
    #                    f"ERR: {err}"
    #         )
    #
    #     if payment is None:
    #         print(f"Payment record not found for Bill No: {edp_bill_no}")
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found")
    #
    #     try:
    #         payment = payment.__dict__
    #
    #         status = payment.get("status")
    #         if status != 'paid':
    #             return None
    #
    #
    #         user_id = payment.get('user_id')
    #         amount = payment.get('amount')
    #         buy_date = payment.get('updated_at')
    #         subs_end_date = payment.get("available_to")
    #
    #         user = self.session.query(models.User).filter_by(user_id=user_id).first().__dict__
    #
    #         promocode = user.get("special_promocode")
    #         username = user.get("username")
    #         reg_date = user.get("created_at")
    #
    #         user_with_subs = models.UsersWithSubs(
    #             promocode=promocode,
    #             amount=amount,
    #             buy_date=buy_date,
    #             subs_end_date=subs_end_date,
    #             user_id=user_id,
    #             username=username,
    #             reg_date=reg_date
    #         )
    #
    #         self.session.add(user_with_subs)
    #         self.session.commit()
    #
    #         return "OK"
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Error occurred while trying to add payment data with payment EDP_BILL_NO '{edp_bill_no}'\n"
    #                    f"ERR: {err}"
    #         )

    def payment_result(self,
                       EDP_PRECHECK: str = Form(None),  # Allow None for the pre-check
                       EDP_BILL_NO: str = Form(...),
                       EDP_REC_ACCOUNT: str = Form(...),
                       EDP_PAYER_ACCOUNT: str = Form(None),  # Payer account only for confirmation
                       EDP_AMOUNT: float = Form(...),
                       EDP_TRANS_ID: str = Form(None),  # Transaction ID only for confirmation
                       EDP_TRANS_DATE: str = Form(None),  # Transaction date only for confirmation
                       EDP_CHECKSUM: str = Form(None),
                       EDP_SIGNATURE: str = Form(None)):  # Signature only for confirmation):  # Status only for confirmation  EDP_STATUS: str = Form(None)

        print(f"EDP_PRECHECK: {EDP_PRECHECK}")
        print(f"EDP_BILL_NO: {EDP_BILL_NO}")
        print(f"EDP_REC_ACCOUNT: {EDP_REC_ACCOUNT}")
        print(f"EDP_PAYER_ACCOUNT: {EDP_PAYER_ACCOUNT}")
        print(f"EDP_AMOUNT: {EDP_AMOUNT}")
        print(f"EDP_TRANS_ID: {EDP_TRANS_ID}")
        print(f"EDP_TRANS_DATE: {EDP_TRANS_DATE}")
        print(f"EDP_CHECKSUM: {EDP_CHECKSUM}")
        print(f"EDP_SIGNATURE: {EDP_SIGNATURE}")


        # --- Handle Pre-check Request (Order Authenticity Confirmation) ---
        if EDP_PRECHECK == "YES":
            print(f"Precheck request for Bill No: {EDP_BILL_NO}")
            try:
                # Check if the order exists and the amount is correct
                payment = self.session.query(models.Payment).filter(models.Payment.order_id == int(EDP_BILL_NO)).first()
            except Exception as err:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error occurred while trying to find the payment with EDP_BILL_NO '{EDP_BILL_NO}'\n"
                           f"Check if the order exists and the amount is correct\n"
                           f"ERR: {err}"
                )

            if payment is None or round(payment.amount, 2) != round(EDP_AMOUNT, 2):
                print(f"Precheck failed for Bill No: {EDP_BILL_NO}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Order not found or amount mismatch")

            # --- Handle Payment Confirmation (After Payment) ---
            print(f"Payment confirmation received for Bill No: {EDP_BILL_NO}")

            return PlainTextResponse(content="OK", status_code=200)
        else:
            # Find the payment record in the database using the bill_no
            try:
                payment = self.session.query(models.Payment).filter(models.Payment.order_id == int(EDP_BILL_NO)).first()
            except Exception as err:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error occurred while trying to find order with EDP_BILL_NO '{EDP_BILL_NO}'\n"
                           f"# Find the payment record in the database using the bill_no\n"
                           f"ERR: {err}"
                )

            if payment is None:
                print(f"Payment record not found for Bill No: {EDP_BILL_NO}")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found")

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
                payment.trans_id = EDP_TRANS_ID  # Store Idram transaction ID
                payment.trans_date = EDP_TRANS_DATE  # Store the transaction date
                payment.payer_account = EDP_PAYER_ACCOUNT  # Store Pyaer Idram account ID

                self.session.commit()
                print(f"Payment {EDP_BILL_NO} marked as paid")
            except Exception as err:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error occurred when EDP_STATUS = 1\n"
                           f"ERR: {err}"
                )

            self.payment_data_to_users_with_subs(EDP_BILL_NO)

            return PlainTextResponse(content="OK", status_code=200)
