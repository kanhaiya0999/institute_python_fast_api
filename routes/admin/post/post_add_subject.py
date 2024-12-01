from bson import ObjectId
from fastapi import APIRouter, Depends

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.SubjectsTypes import SubjectsTypes
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_class_collection, get_subject_collection


router = APIRouter()


@router.post("/api/add_subject")
async def add_subject(details: SubjectsTypes, user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:
    classes_collection = await get_class_collection()
    class_details = classes_collection.find_one(
        {"_id": ObjectId(details.class_name_id)})
    if class_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.CLASS_NOT_FOUND.value,
            is_success=False

        )
    classes_collection = await get_subject_collection()
    classes_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.SUBJECT_ADDED.value,
        is_success=True
    )
