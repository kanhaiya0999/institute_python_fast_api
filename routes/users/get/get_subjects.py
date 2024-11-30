
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_subject_collection


router = APIRouter()


class SubjectType(BaseModel):
    name: str
    id: str


class SubjectTypeResponse(BaseResponse):
    subjects: list[SubjectType]


@router.get("/api/get_subjects")
async def get_subjects(class_name_id: str, user_details: UserRegisterTypes = Depends(authenticate_user)) -> SubjectTypeResponse:
    subjects_collection = await get_subject_collection()
    subjects = subjects_collection.find(
        {"class_name_id": class_name_id}).to_list()

    subjects = [
        SubjectType(
            name=subject["name"],
            id=str(subject["_id"])
        ) for subject in subjects
    ]
    return SubjectTypeResponse(
        status=200,
        message=StatusMessages.SUBJECT_FETCHED.value,
        is_success=True,
        subjects=subjects

    )
