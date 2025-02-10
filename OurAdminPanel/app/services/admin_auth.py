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
from schemas.partner_sellers_schemas import PartnerOut, Token, PartnerLoginForm
from database import get_session
from models import models


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/partner_auth_router/login')


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


def get_current_partner(token: str = Depends(oauth2_schema)):
    try:
        current_partner = PartnerAuthService.verify_token(token)
        return current_partner
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="In UserApp/services/partner_auth.py function get_current_partner()\n"
                                   "Error occurred while trying to get current partner\n"
                                   f"ERR: {err}")


class PartnerAuthService:
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
                                detail="In UserApp/services/admin_auth.py class AuthService, function verify_token()\n"
                                       "Error occurred while trying to create HTTPException\n"
                                       f"ERR: {err}")
        try:
            payload = jwt.decode(
                token,
                "secret",
                algorithms=["HS256"]
            )
        except JWTError:
            raise exception

        try:
            partner_data = payload.get('partner')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function verify_token()\n"
                                       "Error occurred while trying to get user from payload\n"
                                       f"ERR: {err}")

        try:
            partner = PartnerOut.parse_obj(partner_data)
        except ValidationError:
            raise exception

        return partner

    @classmethod
    def create_token(cls, partner):
        try:
            partner_data = PartnerOut.from_orm(partner)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function create_token()\n"
                                       "Error occurred while trying to do user_data = UserOut.from_orm(user)\n"
                                       f"ERR: {err}")

        try:
            now = datetime.datetime.utcnow()
            payload = {
                "exp": now + datetime.timedelta(minutes=1440),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
                "partner": partner_data.dict()
            }
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function create_token()\n"
                                       "Error occurred while trying to make payload\n"
                                       f"ERR: {err}")

        try:
            token = jwt.encode(payload, "secret", algorithm="HS256")
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function create_token()\n"
                                       "Error occurred while trying to create token... jwt.encode(...)\n"
                                       f"ERR: {err}")
        try:
            access_token = Token(access_token=token)
            return access_token
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function create_token()\n"
                                       "Error occurred while trying to create and return Token... Token(token)\n"
                                       f"ERR: {err}")

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def authenticate_partner(self, login_data: PartnerLoginForm):
        try:
            name_or_email = login_data.name_or_email
            password = login_data.password
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function authenticate_user()\n"
                                       "Error occurred while trying to get email and password from login_data\n"
                                       f"ERR: {err}")

        try:
            partner = self.session.query(models.PartnerProgramSeller).filter_by(email=name_or_email).first()
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function authenticate_user()\n"
                                       f"Error occurred while trying to get user by email '{name_or_email}'\n"
                                       f"ERR: {err}")
        if partner is None:
            try:
                partner = self.session.query(models.PartnerProgramSeller).filter_by(name=name_or_email).first()
            except Exception as err:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="In UserApp/services/admin_auth.py class AuthService, function authenticate_user()\n"
                                           f"Error occurred while trying to get user by username '{name_or_email}'\n"
                                           f"ERR: {err}")
            if partner is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with username or email '{name_or_email}' was not found!")

        try:
            password_from_db = partner.__dict__.get('password')
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function authenticate_user()\n"
                                       f"Error occurred while trying to get a password from user taken from database\n"
                                       f"ERR: {err}")

        if password_from_db != login_data.password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Wrong password: '{password}'")

        try:
            access_token = self.create_token(partner)
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/admin_auth.py class AuthService, function authenticate_user()\n"
                                       f"Error occurred while trying to create token...function create_token(...)\n"
                                       f"ERR: {err}")

        return {'token': access_token,
                'promo_code': partner.__dict__.get('special_promo_code'),
                'name': partner.__dict__.get('name')}
