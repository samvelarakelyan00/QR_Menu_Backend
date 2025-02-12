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
from passlib.hash import bcrypt
from jose import jwt, JWTError

# Own
from schemas.auth_schema import Token, CafeAdminLoginForm, CafeAdminOut
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
        current_admin = CafeAdminAuthService.verify_token(token)
        return current_admin
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=err)


class CafeAdminAuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        try:
            result = bcrypt.verify(plain_password, hashed_password)
            return result
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

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
                "cafesecret",
                algorithms=["HS256"]
            )
        except JWTError:
            HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error!"
            )

        try:
            admin_data = payload.get('cafe_admin')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            admin = CafeAdminOut.parse_obj(admin_data)
        except ValidationError:
            raise exception

        return admin

    @classmethod
    def create_token(cls, admin):
        try:
            admin_data = CafeAdminOut.from_orm(admin)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            now = datetime.datetime.utcnow()
            payload = {
                "exp": now + datetime.timedelta(minutes=1440),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
                "cafe_admin": admin_data.dict()
            }
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            token = jwt.encode(payload, "cafesecret", algorithm="HS256")
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

    def authenticate_admin(self, login_data: CafeAdminLoginForm):
        try:
            email = login_data.email
            password = login_data.password
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        try:
            admin = self.session.query(models.HoReKaAdmin).filter_by(email=email).first()
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

        if not self.verify_password(password, password_from_db):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Wrong Data")

        try:
            access_token = self.create_token(admin)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=err)

        return access_token
