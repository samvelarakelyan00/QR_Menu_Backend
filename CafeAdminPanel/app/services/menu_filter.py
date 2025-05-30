from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy import distinct
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

    def get_all_menu_by_lang(self, horekaclient_id: int, lang: str):
        try:
            products = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id)  # First filter
                .filter_by(language=lang)
                .all()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return products

    def get_menu_by_product_id(self, horekaclient_id: int, product_id: int):
        try:
            product = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id)  # First filter
                .filter_by(id=product_id)
                .first()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return product

    def get_menu_by_kind_lang(self, horekaclient_id: int, kind: str, lang: str):
        try:
            menu_by_kind = (
                self.session.query(models.HoReKaMenu)
                .filter_by(horekaclient_id=horekaclient_id)  # First filter
                .filter_by(kind=kind)
                .filter_by(language=lang)
                .all()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return menu_by_kind

    def get_menu_all_kinds(self, horekaclient_id: int):
        try:
            kinds = (
                self.session.query(distinct(models.HoReKaMenu.kind))
                .filter_by(horekaclient_id=horekaclient_id)
                .all()
            )
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return [kind[0] for kind in kinds]

    def get_menu_all_categories(self, horekaclient_id: int, kind: str):
        try:
            categories = (
                self.session.query(distinct(models.HoReKaMenu.category))
                .filter_by(horekaclient_id=horekaclient_id)
                .filter_by(kind=kind)
                .all()
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not categories:
            return []

        return [category[0] for category in categories]
