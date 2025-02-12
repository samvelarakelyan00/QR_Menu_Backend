from fastapi import APIRouter


from .endpoints.admin_auth import router as admin_auth_router


router = APIRouter(
    prefix='/api'
)


router.include_router(admin_auth_router)
