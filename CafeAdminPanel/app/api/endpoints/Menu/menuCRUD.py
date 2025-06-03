import os
import uuid
from typing import Optional

# FastAPI
from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException

from starlette import status

# Own
from schemas.menu_schema import (
    MenuAddNew,
    ProductUpdate,
    ProductImageGet
)

from services.Admin import admin_auth as cafe_admin_auth_service
from services.Menu import menuCRUD as menuCRUD_service
from services.PaymentIDram import horeca_subs_payment_check as payment_check_service

from services import aws_s3 as aws_s3_service


router = APIRouter(
    prefix='/menuCRUD',
    tags=["Menu CRUD"]
)


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
        payment_check_service: payment_check_service.CheckHoReCaSubsPlanService = Depends(),
        current_admin=Depends(cafe_admin_auth_service.get_current_admin)
):
    try:
        current_payment = payment_check_service.check_current_payment(current_admin.__dict__.get("id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if current_payment is None:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED)

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")

        UPLOAD_FOLDER = f"../../../{kind.replace(' ', '')}/{category.replace(' ', '')}"

        # Generate a unique filename
        file_extension = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the image file
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        # IMAGE_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "..", "..", "images"))

        aws_s3_service.s3_manager.upload_file(file_path, 'qrmenuarmeniafilesandimagesbucket',
                                              image.filename+unique_filename,
                                              public_read=True)

        image_src = aws_s3_service.s3_manager.get_public_url('qrmenuarmeniafilesandimagesbucket', image.filename+unique_filename)

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
            "image_src": image_src,  # Store only the filename
        }

        return menu_crud_service.add_menu_new(horekaclient_id, menu_data)

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/all-menu")
def get_all_menu(menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                 payment_check_service: payment_check_service.CheckHoReCaSubsPlanService = Depends(),
                 current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    try:
        current_payment = payment_check_service.check_current_payment(current_admin.__dict__.get("id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if current_payment is None:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED)

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.get_all_menu(horekaclient_id)


@router.put("/update-product/{product_id}")
def update_product(product_id: int,
                   product_update_data: ProductUpdate,
                   menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                   payment_check_service: payment_check_service.CheckHoReCaSubsPlanService = Depends(),
                   current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    try:
        current_payment = payment_check_service.check_current_payment(current_admin.__dict__.get("id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if current_payment is None:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED)

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.update_product(horekaclient_id, product_id, product_update_data)


@router.delete("/delete-product/{product_id}")
def delete_product(product_id: int,
                   menu_crud_service: menuCRUD_service.MenuCRUDService = Depends(),
                   payment_check_service: payment_check_service.CheckHoReCaSubsPlanService = Depends(),
                   current_admin=Depends(cafe_admin_auth_service.get_current_admin)):
    try:
        current_payment = payment_check_service.check_current_payment(current_admin.__dict__.get("id"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if current_payment is None:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED)

    try:
        horekaclient_id = current_admin.__dict__.get("horekaclient_id")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return menu_crud_service.delete_product(horekaclient_id, product_id)
