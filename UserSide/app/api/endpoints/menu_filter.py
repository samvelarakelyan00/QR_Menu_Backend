import os

# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from services import menu_filter as menu_filter_service

from schemas.menu_schema import (
    HoReKaClientResponse,
    ProductImageGet
)


router = APIRouter(
    prefix='/menu-filter',
    tags=["Menu Filter"]
)


@router.get("/by-horekaclient-id/{horekaclient_id}", response_model=HoReKaClientResponse)
def get_menu_by_product_id(horekaclient_id: int,
                           menu_fileter_service: menu_filter_service.MenuFilterService = Depends()
                           ):

    return menu_fileter_service.get_horeka_by_id(horekaclient_id)


@router.get("/all-menu/{horekaclient_id}")
def get_all_menu(horekaclient_id: int,
                 menu_fileter_service: menu_filter_service.MenuFilterService = Depends()):

    return menu_fileter_service.get_all_menu(horekaclient_id)


@router.post("/get-image")
async def get_image(product_image_get_data: ProductImageGet):
    kind = product_image_get_data.kind
    category = product_image_get_data.category
    filename = product_image_get_data.filename
    file_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", ".."))
    file_path = os.path.join(f"{file_path}/{kind}/{category}", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)


@router.get("/by-product-id/{product_id}")
def get_menu_by_product_id(horekaclient_id: int,
                           product_id: int,
                           menu_fileter_service: menu_filter_service.MenuFilterService = Depends()
                           ):

    return menu_fileter_service.get_menu_by_product_id(horekaclient_id, product_id)


@router.get("/by-kind/{kind}/{language}")
def get_menu_by_kind(horekaclient_id: int,
                     kind: str,
                     language: str = 'en',
                     menu_fileter_service: menu_filter_service.MenuFilterService = Depends(),
                     ):

    return menu_fileter_service.get_menu_by_kind(horekaclient_id, kind, language)


@router.get("/by-category/{category}/{language}")
def get_menu_by_kind(horekaclient_id: int,
                     category: str,
                     language: str = 'en',
                     menu_fileter_service: menu_filter_service.MenuFilterService = Depends(),
                     ):

    return menu_fileter_service.get_menu_by_category(horekaclient_id, category, language)


@router.get("/by-price-above/{horekaclient_id}")
def get_menu_by_price_above(horekaclient_id: int,
                           min_price: float = 1200,
                           language: str = 'en',
                           menu_fileter_service: menu_filter_service.MenuFilterService = Depends()):
    """
    Get menu items with price above specified value
    """
    return menu_fileter_service.get_menu_by_price_above(horekaclient_id, min_price, language)


@router.get("/by-nutritional-values/{horekaclient_id}")
def get_menu_by_nutritional_values(horekaclient_id: int,
                                 max_calories: float = 20,
                                 min_weight: float = 100,
                                 min_price: float = 3450,
                                 language: str = 'en',
                                 menu_fileter_service: menu_filter_service.MenuFilterService = Depends()):
    """
    Get menu items filtered by calories, weight, and price
    """
    return menu_fileter_service.get_menu_by_nutritional_values(
        horekaclient_id,
        max_calories,
        min_weight,
        min_price,
        language
    )


