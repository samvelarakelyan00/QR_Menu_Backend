import glob
import os

from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models

from schemas.menu_schema import (
    MenuAddNew,
    ProductUpdate
)

from ..aws_s3 import s3_manager

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class MenuCRUDService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_menu_new(self, horekaclient_id: int, add_menu_new_data: dict):
        try:
            new_menu_add = models.HoReKaMenu(**add_menu_new_data, horekaclient_id=horekaclient_id)

            self.session.add(new_menu_add)
            self.session.commit()

            return "OK"
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_all_menu(self, horekaclient_id):
        try:
            all_menu = self.session.query(models.HoReKaMenu).filter_by(horekaclient_id=horekaclient_id).all()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return all_menu

    def update_product(self, horekaclient_id: int, product_id: int, product_update_data: ProductUpdate):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id, id=product_id)
                .first()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        try:
            update_data = product_update_data.dict(exclude_unset=True)  # Exclude fields that were not provided

            for key, value in update_data.items():
                setattr(product, key, value)  # Dynamically update the model attributes

            self.session.commit()
            self.session.refresh(product)

            return product

        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_product(self, horekaclient_id: int, product_id: int):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id, id=product_id)
                .first()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        try:
            s3_manager.delete_object("qrmenuarmeniafilesandimagesbucket",
                                     dict(product).get("image_src"))

            self.session.delete(product)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
