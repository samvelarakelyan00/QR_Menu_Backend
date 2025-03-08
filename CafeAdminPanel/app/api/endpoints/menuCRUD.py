import os
import sys
import uuid
from typing import Optional

# FastAPI
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from starlette import status

# Own
from schemas.menu_schema import (
    MenuAddNew,
    ProductUpdate,
    ProductImageGet
)

from services import admin_auth as cafe_admin_auth_service
from services import menuCRUD as menuCRUD_service


router = APIRouter(
    prefix='/menuCRUD',
    tags=["Menu CRUD"]
)


# @router.post("/add-menu-new")
# def add_menu_new(menu_new_data: MenuAddNew,
#                 menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
#                 current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
#
#     try:
#         horekaclient_id = current_admin.__dict__.get("horekaclient_id")
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=err
#         )
#
#     return menu_crud_service.add_menu_new(horekaclient_id, menu_new_data)


@router.post("/add-menu-new")
async def add_menu_new(
        kind: str = Form(...),
        category: str = Form(...),
        name: str = Form(...),
        quantity: str = Form(...),
        price: float = Form(...),
        description: str = Form(...),
        language: str = Form(...),
        preparation_time: Optional[float] = Form(None),
        weight: Optional[float] = Form(None),
        calories: Optional[float] = Form(None),
        image: UploadFile = File(...),
        menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
        current_admin=Depends(cafe_admin_auth_service.get_current_admin)
):
    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")

        UPLOAD_FOLDER = f"../../../{kind}/{category}/"
        # Generate a unique filename
        file_extension = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the image file
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        # Prepare menu data
        menu_data = {
            "kind": kind,
            "category": category,
            "name": name,
            "quantity": quantity,
            "price": price,
            "description": description,
            "language": language,
            "preparation_time": preparation_time,
            "weight": weight,
            "calories": calories,
            "image_src": unique_filename,  # Store only the filename
        }

        return menu_crud_service.add_menu_new(horekaclient_id, menu_data)

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        )


@router.post("/get-image")
async def get_image(product_image_get_data: ProductImageGet,
                    current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    kind = product_image_get_data.kind
    category = product_image_get_data.category
    filename = product_image_get_data.filename
    file_path = os.path.abspath(os.path.join(os.getcwd(), "..", "..", ".."))
    file_path = os.path.join(f"{file_path}/{kind}/{category}", filename)
    print(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)


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
