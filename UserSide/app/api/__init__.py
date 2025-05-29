from fastapi import APIRouter

from .endpoints.menu_filter import router as menu_filter_router
from .endpoints.user import router as user_router
from .endpoints.payment_idram import router as payment_idram_router

from .endpoints.auth import router as user_auth_router

from .endpoints.horeka_reservation import router as reservation_router

from .endpoints.terms import router as termsCRUD_router


router = APIRouter(
    prefix='/api'
)

router.include_router(menu_filter_router)
router.include_router(user_router)
router.include_router(payment_idram_router)

router.include_router(user_auth_router)
router.include_router(reservation_router)

router.include_router(termsCRUD_router)


