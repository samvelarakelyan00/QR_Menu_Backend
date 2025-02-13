from fastapi import APIRouter


from .endpoints.admin_auth import router as admin_auth_router
from .endpoints.menuCRUD import router as menuCRUD_router
from .endpoints.menu_filter import router as menu_filter_router


router = APIRouter(
    prefix='/api'
)


router.include_router(admin_auth_router)
router.include_router(menuCRUD_router)
router.include_router(menu_filter_router)
