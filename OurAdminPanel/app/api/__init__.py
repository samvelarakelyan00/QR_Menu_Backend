from fastapi import APIRouter


from .endpoints.admin_auth import router as admin_auth_router
from .endpoints.horekaCRUD import router as horekaCRUD_router
from .endpoints.horekaAdminCRUD import router as horekaAdminCRUD_router
from .endpoints.terms import router as termsCRUD_router
from .endpoints.subs_plan_crud import router as subs_plan_CRUD_router


router = APIRouter(
    prefix='/api'
)


router.include_router(admin_auth_router)
router.include_router(horekaCRUD_router)
router.include_router(horekaAdminCRUD_router)
router.include_router(termsCRUD_router)
router.include_router(subs_plan_CRUD_router)
