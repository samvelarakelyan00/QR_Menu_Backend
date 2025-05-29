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


class TermsServiceCRUD:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_term(self, lang: str, kind: str):
        try:
            term_data = (self.session.query(models.TermText)
                         .filter(models.TermText.language==lang, models.TermText.term_kind==kind)
                         .first())
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        if term_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        return term_data
