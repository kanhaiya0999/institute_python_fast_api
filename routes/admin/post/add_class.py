from fastapi import APIRouter, Request
from fastapi import Depends
from models.UserRegisterTypes import UserRegisterTypes
from models.BaseResponse import BaseResponse
from models.ClassesTypes import ClassesTypes
from models.StatusMessages import StatusMessages
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_class_collection


router = APIRouter()


@router.post("/api/add_class")
async def add_class(details: ClassesTypes, request: Request, user_details: UserRegisterTypes = Depends(authenticate_user)) -> BaseResponse:

    if user_details.type != 'admin':
        return BaseResponse(
            status=401,
            message=StatusMessages.UNAUTHORIZED.value,
            is_success=False

        )
    classes_collection = await get_class_collection()
    classes_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.CLASS_ADDED.value,
        is_success=True
    )