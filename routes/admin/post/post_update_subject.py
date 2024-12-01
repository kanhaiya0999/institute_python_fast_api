from bson import ObjectId
from fastapi import APIRouter, Depends

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.SubjectsTypes import SubjectsTypes
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_subject_collection

router = APIRouter()


class UpdateSubjectType(SubjectsTypes):
    id: str


@router.post("/api/update_subject")
async def update_subject(details: UpdateSubjectType,  user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:
    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.id)})
    print(subject_details)
    if subject_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.SUBJECT_NOT_FOUND.value,
            is_success=False
        )

    subjects_collection.update_one({"_id": ObjectId(details.id)}, {
        "$set": {"name": details.name, }})
    return BaseResponse(
        status=200,
        message=StatusMessages.SUBJECT_UPDATED.value,
        is_success=True
    )
