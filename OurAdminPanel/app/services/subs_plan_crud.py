from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy import text
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models

from schemas.subs_plan_schema import (
    HoReCaSubsPlanCreateSchema,
    HoReCaSubsPlanUpdateSchema
)


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class HoReCaSubsPlanCRUD:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_new_horeca_subs_plan(self, subs_plan_data: HoReCaSubsPlanCreateSchema):
        try:
            subs_plan = models.HoReCaSubsPlan(**subs_plan_data.__dict__)
            self.session.add(subs_plan)
            self.session.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_available_subs_plans(self):
        try:
            subs_plans = self.session.query(models.HoReCaSubsPlan).all()

            return subs_plans
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_subs_plan_by_name(self, name: str):
        try:
            subs_plan = self.session.query(models.HoReCaSubsPlan).filter_by(name=name).first()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if subs_plan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return subs_plan

    def update_subs_plan(self, subs_plan_id: int, subs_plan_update_data: HoReCaSubsPlanUpdateSchema):
        try:
            subs_plan = self.session.query(models.HoReCaSubsPlan).filter_by(id=subs_plan_id).first()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if subs_plan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        try:
            update_data = subs_plan_update_data.dict(exclude_unset=True)  # Exclude fields that were not provided

            for key, value in update_data.items():
                setattr(subs_plan, key, value)  # Dynamically update the model attributes

            self.session.commit()
            self.session.refresh(subs_plan)

            return subs_plan
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_subs_plan(self, subs_plan_id: int):
        try:
            subs_plan = self.session.query(models.HoReCaSubsPlan).filter_by(id=subs_plan_id).first()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if subs_plan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        try:
            self.session.delete(subs_plan)
            self.session.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
