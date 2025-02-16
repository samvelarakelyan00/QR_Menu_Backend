from fastapi import Depends, status
from fastapi.exceptions import HTTPException

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


class MenuFilterService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_horeka_by_id(self, horekaclient_id: int):
        try:
            horeka = self.session.query(models.HoReKaClient).filter_by(id=horekaclient_id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if not horeka:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="horeka client not found"
            )

        return horeka

    def get_menu_by_product_id(self, horekaclient_id: int, product_id: int):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id)  # First filter
                .filter_by(id=product_id)
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

        return product

    def get_menu_by_kind(self, horekaclient_id: int, kind: str, language: str = 'en'):
        try:
            menu_by_kind = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id)  # First filter
                .filter_by(kind=kind)
                .filter_by(language=language)
                .all()
            )
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        return menu_by_kind

    # def get_menu_by_kind(self, horekaclient_id: int, kind: str):
    #     try:
    #         menu_by_kind = (
    #             self.session.query(models.HoReKaMenu)
    #             .filter_by(horekaclient_id=horekaclient_id)  # First filter
    #             .filter_by(kind=kind)
    #             .all()
    #         )
    #     except Exception as err:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=str(err)
    #         )
    #
    #     return menu_by_kind
