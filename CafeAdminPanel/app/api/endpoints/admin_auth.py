# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.auth_schema import (
    CafeAdminOut,
    Token,
    CafeAdminLoginForm,
)

from services import admin_auth as cafe_admin_auth_service


router = APIRouter(
    prefix='/admin-auth',
    tags=["Cafe Admin Auth"]
)


@router.post("/login", response_model=Token)
def login(login_data: CafeAdminLoginForm,
          service: cafe_admin_auth_service.CafeAdminAuthService = Depends()):

    return service.authenticate_admin(login_data)
