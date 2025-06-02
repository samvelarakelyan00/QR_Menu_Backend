import hashlib

from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi import status, Depends, Form

# SqlAlchemy
from sqlalchemy import desc, func
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

    def find_horeka_admin(self, horeka_admin_id: int):
        try:
            horeka_admin = self.session.query(models.HoReKaAdmin).filter(models.HoReKaAdmin.id == horeka_admin_id).first()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if horeka_admin is None:
            self.session.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return horeka_admin

    def get_horeca_admin_last_payment(self, horeca_admin_id: int):
        horeca_admin = self.find_horeka_admin(horeca_admin_id)

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

        return last_payment

# ===========================   TODO payment statrt order_id 10+ got error   =========================================



# class IDramPaymentService: # TODO
#     def __init__(self, session: Session = Depends(get_session)):
#         self.session = session
#


#     #
#     # def check_user_payment(self, user_id):
#     #     try:
#     #         usr = self.session.query(models.User).filter_by(user_id=user_id).first()
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=err
#     #         )
#     #
#     #     if usr is None:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_404_NOT_FOUND,
#     #             detail=f"User with id '{user_id}' was not found!"
#     #         )
#     #
#     #     usr = usr.__dict__
#     #
#     #     try:
#     #         is_user_free = self.session.query(models.FreeUsers).filter_by(email=usr.get('email')).first()
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=err
#     #         )
#     #
#     #     if (not is_user_free is None and
#     #             is_user_free.__dict__.get("end_date") >= datetime.datetime.now() + datetime.timedelta(hours=4)):
#     #         return True
#     #
#     #     last_payment = self.get_user_last_payment(user_id)
#     #     if last_payment is None:
#     #         return False
#     #
#     #     last_payment = last_payment.__dict__
#     #
#     #     current_datetime = datetime.datetime.now() + datetime.timedelta(hours=4)
#     #     payment_available_to = last_payment.get("available_to")
#     #
#     #     if payment_available_to < current_datetime:
#     #         return False
#     #
#     #     return True
#     #
#     def get_next_order_id(self):
#         # Query the maximum current order_id and increment by 1
#         max_order_id = self.session.query(func.max(models.PaymentIDram.order_id)).scalar()
#         return (max_order_id or 0) + 1
#     #
#     # def get_required_payment_amount(self, user_id):
#     #     # Find Required payment amount
#     #     try:
#     #         user = self.session.query(models.User).filter_by(user_id=user_id).first()
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=err
#     #         )
#     #
#     #     if user is None:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_404_NOT_FOUND,
#     #             detail=f"User with id '{user_id}' was not found!"
#     #         )
#     #
#     #     user = user.__dict__
#     #     special_promocode = user.get("special_promocode")
#     #
#     #     try:
#     #         partner = self.session.query(models.PartnerProgramSeller).filter_by(special_promo_code=special_promocode).first()
#     #     except Exception as err:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #             detail=err
#     #         )
#     #
#     #     if partner is None:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_404_NOT_FOUND,
#     #             detail=f"Partner with promo code '{special_promocode}' was not found!"
#     #         )
#     #
#     #     partner = partner.__dict__
#     #
#     #     return {
#     #         "promocode": partner.get("special_promo_code"),
#     #         "price": partner.get("price")
#     #     }
#     #
#     # def get_payment_amount_by_subs_plan(self):
#     #     try:
#     #         all_data = self.session.query(models.GoldnSipSubsPlans).all()
#     #         return all_data
#     #     except Exception as err:
#     #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #                             detail=err)
#

#
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
