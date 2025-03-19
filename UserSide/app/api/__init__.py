from fastapi import APIRouter

from .endpoints.menu_filter import router as menu_filter_router
from .endpoints.user import router as user_router


router = APIRouter(
    prefix='/api'
)

router.include_router(menu_filter_router)
router.include_router(user_router)
