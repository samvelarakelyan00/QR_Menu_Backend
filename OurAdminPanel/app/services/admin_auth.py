# Standard
import datetime

# FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from pydantic import ValidationError
from fastapi.security.oauth2 import OAuth2PasswordBearer

# SqlAlchemy
from sqlalchemy.orm.session import Session

# Security
from jose import jwt, JWTError

# Own
from schemas.auth_schema import Token, AdminLoginForm, AdminOut
from database import get_session
from models import models


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/admin_auth/login')


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


def get_current_admin(token: str = Depends(oauth2_schema)):
    try:
        current_admin = AdminAuthService.verify_token(token)
        return current_admin
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=err)


class AdminAuthService:
    @classmethod
    def verify_token(cls, token: str):
        try:
            exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate credentials",
                headers={
                    "WWW-Authenticated": 'Bearer'
                }
            )
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)
        try:
            payload = jwt.decode(
                token,
                "secret",
                algorithms=["HS256"]
            )
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=exception
            )

        try:
            admin_data = payload.get('admin')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            admin = AdminOut.parse_obj(admin_data)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        return admin

    @classmethod
    def create_token(cls, admin):
        try:
            admin_data = AdminOut.from_orm(admin)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            now = datetime.datetime.utcnow()
            payload = {
                "exp": now + datetime.timedelta(minutes=1440),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
                "admin": admin_data.dict()
            }
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            token = jwt.encode(payload, "secret", algorithm="HS256")
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)
        try:
            access_token = Token(access_token=token)
            return access_token
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def authenticate_admin(self, login_data: AdminLoginForm):
        try:
            email = login_data.email
            password = login_data.password
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            admin = self.session.query(models.OurAdmin).filter_by(email=email).first()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)
        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Wrong Data")

        try:
            password_from_db = admin.__dict__.get('password')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        if password_from_db != login_data.password:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Wrong Data")

        try:
            access_token = self.create_token(admin)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        return access_token
