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

    def add_menu_new(self, horekaclient_id: int, add_menu_new_data: MenuAddNew):
        try:
            new_menu_add = models.HoReKaMenu(**add_menu_new_data.dict(), horekaclient_id=horekaclient_id)

            self.session.add(new_menu_add)
            self.session.commit()

            return "OK"
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err
            )

    def get_all_menu(self, horekaclient_id):
        try:
            all_menu = self.session.query(models.HoReKaMenu).filter_by(horekaclient_id=horekaclient_id).all()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err
            )

        return all_menu

    def update_product(self, horekaclient_id: int, product_id: int, product_update_data: ProductUpdate):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id, id=product_id)
                .first()
            )
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        try:
            update_data = product_update_data.dict(exclude_unset=True)  # Exclude fields that were not provided
            print(update_data)

            for key, value in update_data.items():
                setattr(product, key, value)  # Dynamically update the model attributes

            self.session.commit()
            self.session.refresh(product)

            return product

        except Exception as err:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    def delete_product(self, horekaclient_id: int, product_id: int):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id, id=product_id)
                .first()
            )
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        try:
            self.session.delete(product)
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
