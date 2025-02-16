# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from services import menu_filter as menu_filter_service

from schemas.menu_schema import (
    HoReKaClientResponse
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


@router.get("/by-product-id/{product_id}")
def get_menu_by_product_id(horekaclient_id: int,
                           product_id: int,
                           menu_fileter_service: menu_filter_service.MenuFilterService = Depends()
                           ):

    return menu_fileter_service.get_menu_by_product_id(horekaclient_id, product_id)


@router.get("/by-kind/{kind}")
def get_menu_by_kind(horekaclient_id: int,
                     kind: str,
                     menu_fileter_service: menu_filter_service.MenuFilterService = Depends(),
                     ):

    return menu_fileter_service.get_menu_by_kind(horekaclient_id, kind)


# @router.get("/by-kind/{kind}/{language}")
# def get_menu_by_kind(horekaclient_id: int,
#                      kind: str,
#                      language: str = 'en',
#                      menu_fileter_service: menu_filter_service.MenuFilterService = Depends(),
#                      ):
#
#     return menu_fileter_service.get_menu_by_kind(horekaclient_id, kind, language)
