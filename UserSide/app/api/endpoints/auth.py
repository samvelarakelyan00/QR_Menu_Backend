import os

# FastAPI
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

# Own
from schemas.auth_schemas import (
    UserCreate,
    UserOut,
    Token,
    LoginForm,
    UserResentEmailVerify
)

from services import auth as auth_service


router = APIRouter(
    prefix='/auth',
    tags=["User Auth"]
)


# @router.post("/sign-up")  # , response_model=UserOut
# def sign_up(user_data: UserCreate,
#             service: auth_service.AuthService = Depends()):
#
#     return service.register_new_user(user_data)
#
#
# @router.post('/resend-email-verification-mail')
# def resend_email_verification_mail(
#     user_data: UserResentEmailVerify,
#     service: auth_service.AuthService = Depends()
# ):
#     return service.resend_email_verification(user_data)
#
#
# @router.get("/verify-user/{user_email}")
# def verify_user(user_email: str,
#                 service: auth_service.AuthService = Depends()):
#
#     service.verify_user(user_email)
#
#     return RedirectResponse("https://goldnsip.am/log")


@router.post("/login")
def login(login_data: LoginForm,
          service: auth_service.AuthService = Depends()):

    return service.authenticate_user(login_data)
