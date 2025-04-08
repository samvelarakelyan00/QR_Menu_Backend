from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic.v1 import NoneIsAllowedError

# SqlAlchemy
from sqlalchemy import text
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models



CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class AdminService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_horeka_admin_by_id(self, admin_id: int):
        try:
            horeka_admin = self.session.query(models.HoReKaAdmin).filter_by(id=admin_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if horeka_admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"HoReKa admin with id '{admin_id}' was not found!"
            )

        return horeka_admin


    def get_horeka_admin_my_account_page_info(self, admin_id: int):
        try:
            horeka_admin = self.session.query(models.HoReKaAdmin).filter_by(id=admin_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if horeka_admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"HoReKa admin with id '{admin_id}' was not found!"
            )

        horeka_admin = horeka_admin.__dict__
        horeka_client_id = horeka_admin.get("horekaclient_id")

        try:
            horeka_client = self.session.query(models.HoReKaClient).filter_by(id=horeka_client_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if horeka_client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"HoReKa client with id '{horeka_client_id}' was not found!"
            )

        # Get HoReKa client total tips amount (only unpaid ones)
        try:
            horeka_client_tips = self.session.execute(
                text("""
                    SELECT horeka_part, updated_at, waiter_id 
                    FROM payments_idram_user_basic_tip
                    WHERE horeka_client_id = :client_id 
                      AND status = 'paid' 
                      AND horeka_part_paid = false
                """),
                {"client_id": horeka_client_id}
            ).mappings().all()

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        total_sum_horeka_part = sum(item["horeka_part"] for item in horeka_client_tips)

        horeka_client = horeka_client.__dict__


        info = {
                    "horeka_name": horeka_client.get("name"),
                    "admin_name": horeka_admin.get("name"),
                    "admin_email": horeka_admin.get("email"),
                    "total_sum_amount": total_sum_horeka_part,
                    "horeka_client_tips": horeka_client_tips
                }

        return info
