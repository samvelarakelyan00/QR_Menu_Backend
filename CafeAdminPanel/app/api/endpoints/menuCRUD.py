# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# Own
from schemas.menu_schema import (
    MenuAddNew,
    ProductUpdate
)

from services import admin_auth as cafe_admin_auth_service
from services import menuCRUD as menuCRUD_service


router = APIRouter(
    prefix='/menuCRUD',
    tags=["Menu CRUD"]
)


@router.post("/add-menu-new")
def add_menu_new(menu_new_data: MenuAddNew,
                menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.add_menu_new(horekaclient_id, menu_new_data)


@router.get("/all-menu")
def get_all_menu(menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                 current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.get_all_menu(horekaclient_id)


@router.put("/update-product/{product_id}")
def update_product(product_id: int,
                   product_update_data: ProductUpdate,
                   menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                   current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.update_product(horekaclient_id, product_id, product_update_data)


@router.delete("/delete-product/{product_id}")
def delete_product(product_id: int,
                   menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                   current_admin=Depends(cafe_admin_auth_service.get_current_admin)):

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

    return menu_crud_service.delete_product(horekaclient_id, product_id)
