from fastapi import APIRouter


from .endpoints.admin_auth import router as admin_auth_router
from .endpoints.menuCRUD import router as menuCRUD_router
from .endpoints.menu_filter import router as menu_filter_router
from .endpoints.admin import router as admin_router
from .endpoints.PaymentIDram.payment_idram import router as idrm_payment_router
from .endpoints.PaymentIDram.horeca_subs_payment_check import router as idram_payment_check_router


router = APIRouter(
    prefix='/api'
)


router.include_router(admin_auth_router)
router.include_router(menuCRUD_router)
router.include_router(menu_filter_router)
router.include_router(admin_router)
router.include_router(idrm_payment_router)
router.include_router(idram_payment_check_router)
