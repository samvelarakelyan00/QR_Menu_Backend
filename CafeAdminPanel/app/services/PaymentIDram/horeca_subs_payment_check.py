import datetime

from fastapi.exceptions import HTTPException
from fastapi import status, Depends

# SqlAlchemy
from sqlalchemy import desc
from sqlalchemy import and_
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


class CheckHoReCaSubsPlanService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def find_horeca_admin(self, horeca_admin_id: int):
        try:
            horeca_admin = self.session.query(models.HoReKaAdmin).filter(models.HoReKaAdmin.id==horeca_admin_id).first()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if horeca_admin is None:
            self.session.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return horeca_admin

    def check_current_payment(self, horeca_admin_id):

        horeca_admin = self.find_horeca_admin(horeca_admin_id)

        try:
            horeca_client_id = horeca_admin.__dict__.get("horekaclient_id")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            last_payment = (self.session.query(models.Payment)
                            .filter(and_(models.Payment.horeka_client_id == horeca_client_id,
                                         models.Payment.status == 'paid'))
                            .order_by(desc(models.Payment.updated_at))
                            .first())
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if last_payment is None or\
           last_payment.__dict__.get("available_to") <= datetime.datetime.now() + datetime.timedelta(hours=4):
            return None

        return last_payment


#     # def payment_data_to_users_with_subs(self, edp_bill_no):
#     #     # ============== Store needed data to users_with_subs ===============
#     #     try:
#     #         # Check if the order exists and the amount is correct
#     #         payment = self.session.query(models.PaymentIDram).filter(models.PaymentIDram.order_id == int(edp_bill_no)).first()
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=f"Error occurred while trying to find the payment with EDP_BILL_NO '{edp_bill_no}'\n"
#     #                    f"Check if the order exists and the amount is correct\n"
#     #                    f"ERR: {err}"
#     #         )
#     #
#     #     if payment is None:
#     #         print(f"PaymentIDram record not found for Bill No: {edp_bill_no}")
#     #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentIDram record not found")
#     #
#     #     try:
#     #         payment = payment.__dict__
#     #
#     #         status = payment.get("status")
#     #         if status != 'paid':
#     #             return None
#     #
#     #
#     #         user_id = payment.get('user_id')
#     #         amount = payment.get('amount')
#     #         buy_date = payment.get('updated_at')
#     #         subs_end_date = payment.get("available_to")
#     #
#     #         user = self.session.query(models.User).filter_by(user_id=user_id).first().__dict__
#     #
#     #         promocode = user.get("special_promocode")
#     #         username = user.get("username")
#     #         reg_date = user.get("created_at")
#     #
#     #         user_with_subs = models.UsersWithSubs(
#     #             promocode=promocode,
#     #             amount=amount,
#     #             buy_date=buy_date,
#     #             subs_end_date=subs_end_date,
#     #             user_id=user_id,
#     #             username=username,
#     #             reg_date=reg_date
#     #         )
#     #
#     #         self.session.add(user_with_subs)
#     #         self.session.commit()
#     #
#     #         return "OK"
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=f"Error occurred while trying to add payment data with payment EDP_BILL_NO '{edp_bill_no}'\n"
#     #                    f"ERR: {err}"
#     #         )
#
