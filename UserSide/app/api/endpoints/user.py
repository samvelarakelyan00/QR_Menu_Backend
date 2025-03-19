import os

# FastAPI
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from services import user as user_service

from schemas.user_schemas import (
    UserFeedbackSchema
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
