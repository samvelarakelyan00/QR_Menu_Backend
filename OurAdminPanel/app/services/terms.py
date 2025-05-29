from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy.orm.session import Session


# Own
from database import get_session
from models import models


from schemas.terms_schema import (
    TermCreateSchema
)

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

    def create_term(self, term_create_data: TermCreateSchema):
        try:
            new_term = models.TermText(**term_create_data.dict())
            print(new_term.__dict__)

            self.session.add(new_term)
            self.session.commit()

            return "OK"
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err
            )
