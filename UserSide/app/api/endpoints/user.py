import os

# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from services import user as user_service

from schemas.user_schemas import (
    UserFeedbackSchema,
    TipPayInfo,
    TipIdramLastButtonInfo
)


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.post("/feedback")
def get_menu_by_product_id(user_feedback_data: UserFeedbackSchema,
                           user_service: user_service.UserService = Depends()
                        ):

        return user_service.user_feedback(user_feedback_data)


@router.post("/tip-page-click-info")
def get_menu_by_product_id(tip_pay_info_data: TipPayInfo,
                           user_service: user_service.UserService = Depends()
                        ):

        return user_service.get_tip_pay_info(tip_pay_info_data)


@router.post("/tip-idram-last-button-click-info")
def get_menu_by_product_id(tip_idram_last_button_data: TipIdramLastButtonInfo,
                           user_service: user_service.UserService = Depends()
                        ):

        return user_service.get_tip_idram_last_button_info(tip_idram_last_button_data)
