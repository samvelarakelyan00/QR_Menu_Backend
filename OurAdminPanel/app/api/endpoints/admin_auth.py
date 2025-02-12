# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.auth_schema import (
    AdminOut,
    Token,
    AdminLoginForm,
)

from services import admin_auth as admin_auth_service


router = APIRouter(
    prefix='/admin-auth',
    tags=["Admin Auth"]
)


@router.post("/login", response_model=Token)
def login(login_data: AdminLoginForm,
          service: admin_auth_service.AdminAuthService = Depends()):

    return service.authenticate_admin(login_data)
