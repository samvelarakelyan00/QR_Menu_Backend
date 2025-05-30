# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
from services import admin_auth as cafe_admin_auth_service
from services import menu_filter as menu_filter_service


router = APIRouter(
    prefix='/menu-filter',
    tags=["Menu Filter"]
)


@router.get("/all/by-lang/{lang}")
def get_all_menu_by_lang(lang: str,
                     menu_crud_service: menu_filter_service.MenuFilterService = Depends(),
                     current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.get_all_menu_by_lang(horekaclient_id, lang)


@router.get("/by-product-id/{product_id}")
def get_menu_by_product_id(product_id: int,
                     menu_crud_service: menu_filter_service.MenuFilterService = Depends(),
                     current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.get_menu_by_product_id(horekaclient_id, product_id)


@router.get("/by-kind/by-lang/{kind}/{lang}")
def get_menu_by_kind(kind: str,
                     lang: str,
                     menu_crud_service: menu_filter_service.MenuFilterService = Depends(),
                     current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.get_menu_by_kind_lang(horekaclient_id, kind, lang)


@router.get("/get-menu-all-kinds")
def get_menu_all_kinds(
                menu_filter_service: menu_filter_service.MenuFilterService = Depends(),
                current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_filter_service.get_menu_all_kinds(horekaclient_id)


@router.get("/get-menu-categories-by-kind/{kind}")
def get_menu_all_categories(
                kind: str,
                menu_filter_service: menu_filter_service.MenuFilterService = Depends(),
                current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_filter_service.get_menu_all_categories(horekaclient_id, kind)
