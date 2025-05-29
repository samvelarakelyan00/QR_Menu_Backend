# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.terms_schema import (
    TermCreateSchema
)

from services import admin_auth as admin_auth_service
from services import terms as terms_curd_service


router = APIRouter(
    prefix='/termsCRUD',
    tags=["Terms CRUD"]
)


@router.post("/add-term")
def add_term(term_create_data: TermCreateSchema,
             service: terms_curd_service.TermsServiceCRUD = Depends(),
             current_admin=Depends(admin_auth_service.get_current_admin)):

    return service.create_term(term_create_data)


@router.get("/term/by-lang/by-kind/{lang}/{kind}")
def add_term(lang: str,
             kind: str,
             service: terms_curd_service.TermsServiceCRUD = Depends(),
             current_admin=Depends(admin_auth_service.get_current_admin)):

    return service.get_term(lang, kind)
