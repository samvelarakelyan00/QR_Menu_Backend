import datetime

from pydantic import ValidationError

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

from jose import jwt, JWTError

from schemas import Token, UserOut


oauth2_schema = OAuth2PasswordBearer(tokenUrl='../main/login')

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


def create_token(user):
    try:
        user_data = UserOut.from_orm(user)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="In UserApp/services/auth.py class AuthService, function create_token()\n"
                                   "Error occurred while trying to do user_data = UserOut.from_orm(user)\n"
                                   f"ERR: {err}")

    try:
        now = datetime.datetime.utcnow()
        payload = {
            "exp": now + datetime.timedelta(minutes=10),  # 1440 min -> 1 day, (max av. -> 43200, 1 month)
            "user": user_data.dict()
        }
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="In UserApp/services/auth.py class AuthService, function create_token()\n"
                                   "Error occurred while trying to make payload\n"
                                   f"ERR: {err}")

    try:
        token = jwt.encode(payload, "secret", algorithm="HS256")
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="In UserApp/services/auth.py class AuthService, function create_token()\n"
                                   "Error occurred while trying to create token... jwt.encode(...)\n"
                                   f"ERR: {err}")
    try:
        access_token = Token(access_token=token)
        return access_token
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="In UserApp/services/auth.py class AuthService, function create_token()\n"
                                   "Error occurred while trying to create and return Token... Token(token)\n"
                                   f"ERR: {err}")


def verify_token(token: str):
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
                            detail="In UserApp/services/auth.py class AuthService, function verify_token()\n"
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
        user_data = payload.get('user')
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="In UserApp/services/auth.py class AuthService, function verify_token()\n"
                                   "Error occurred while trying to get user from payload\n"
                                   f"ERR: {err}")

    try:
        user = UserOut.parse_obj(user_data)
    except ValidationError:
        raise exception

    return user


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        current_user = verify_token(token)
        return current_user
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="In UserApp/services/auth.py function get_current_user()\n"
                                   "Error occurred while trying to get current user\n"
                                   f"ERR: {err}")
