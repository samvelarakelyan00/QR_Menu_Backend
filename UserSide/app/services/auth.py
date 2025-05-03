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
from schemas.auth_schemas import UserOut, Token, UserCreate, LoginForm, UserResentEmailVerify
from database import get_session
from models import models
from . import mails_send


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        current_user = AuthService.verify_token(token)
        return current_user
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="In UserApp/services/auth.py function get_current_user()\n"
                                   "Error occurred while trying to get current user\n"
                                   f"ERR: {err}")


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def authenticate_user(self, login_data: LoginForm):
        try:
            username_or_email = login_data.username_or_email
            password = login_data.password
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="In UserApp/services/auth.py class AuthService, function authenticate_user()\n"
                                       "Error occurred while trying to get email and password from login_data\n"
                                       f"ERR: {err}")

        return "OK"
