from fastapi import APIRouter


from .endpoints.admin_auth import router as admin_auth_router
from .endpoints.horekaCRUD import router as horekaCRUD_router
from .endpoints.horekaAdminCRUD import router as horekaAdminCRUD_router


router = APIRouter(
    prefix='/api'
)


router.include_router(admin_auth_router)
router.include_router(horekaCRUD_router)
router.include_router(horekaAdminCRUD_router)
