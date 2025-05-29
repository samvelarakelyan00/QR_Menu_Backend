# FastAPI
from fastapi import APIRouter, Depends

from services import terms as terms_curd_service


router = APIRouter(
    prefix='/termsCRUD',
    tags=["Terms CRUD"]
)


@router.get("/term/by-lang/by-kind/{lang}/{kind}")
def get_term(lang: str,
             kind: str,
             service: terms_curd_service.TermsServiceCRUD = Depends()):

    return service.get_term(lang, kind)
