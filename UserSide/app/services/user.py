from fastapi import Depends, status
from fastapi.exceptions import HTTPException

# SqlAlchemy
from sqlalchemy.orm.session import Session

# Own
from database import get_session
from models import models

from schemas.user_schemas import (
    UserScanQRSchema,
    UserFeedbackSchema
)


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def scan_qr_info(self, scan_data: UserScanQRSchema):
        try:
            scan = models.QRScanInfo(**dict(scan_data))
            self.session.add(scan)
            self.session.commit()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        return "OK"


    def user_feedback(self, user_feedback_data: UserFeedbackSchema):
        try:
            horeka_client_id = user_feedback_data.horeka_client_id
            rating = user_feedback_data.rating
            feedback_text = user_feedback_data.feedback_text
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        try:
            feedback = models.UserFeedback(**dict(user_feedback_data))
            self.session.add(feedback)
            self.session.commit()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

        return "OK"