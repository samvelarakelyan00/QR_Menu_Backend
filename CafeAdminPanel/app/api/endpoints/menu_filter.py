# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
from schemas.menu_schema import (
    MenuAddNew
)

from services import admin_auth as cafe_admin_auth_service
from services import menu_filter as menu_filter_service


router = APIRouter(
    prefix='/menu-filter',
    tags=["Menu Filter"]
)


@router.get("/by-product-id/{product_id}")
def get_menu_by_product_id(product_id: int,
                     menu_crud_service: menu_filter_service.MenuFilterService = Depends(),
                     current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.get_menu_by_product_id(horekaclient_id, product_id)


@router.get("/by-kind/{kind}")
def get_menu_by_kind(kind: str,
                     menu_crud_service: menu_filter_service.MenuFilterService = Depends(),
                     current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.get_menu_by_kind(horekaclient_id, kind)
