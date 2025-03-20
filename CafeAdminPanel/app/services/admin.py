from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic.v1 import NoneIsAllowedError

# SqlAlchemy
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

        horeka_client = horeka_client.__dict__


        try:  # TODO get correct subs plan data, have or not yet, last subs plan and right check available_to
            horeka_client_subs_plan_data = self.session.query(models.Payment).filter_by(horeka_client_id=horeka_client_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if horeka_client_subs_plan_data is not None:  # TODO get correct subs plan data, have or not yet, last subs plan and right check available_to
            horeka_client_subs_plan_data = horeka_client_subs_plan_data.__dict__
            horeka_subs_plan = horeka_client_subs_plan_data.get("subs_plan")
            horeka_subs_plan_expires = horeka_client_subs_plan_data.get("available_to")
        else:
            horeka_subs_plan = None
            horeka_subs_plan_expires = None


        info = {
            "horeka_name": horeka_client.get("name"),
            "admin_name": horeka_admin.get("name"),
            "admin_email": horeka_admin.get("email"),
            "horeka_subs_plan": horeka_subs_plan,
            "horeka_subs_plan_expires": horeka_subs_plan_expires
        }

        return info
