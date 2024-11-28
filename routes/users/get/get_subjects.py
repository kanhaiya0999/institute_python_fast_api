
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.GetSubjectsTypes import GetSubjectsTypes
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


@router.post("/api/get_subjects")
async def get_subjects(details: GetSubjectsTypes, request: Request, user_details: UserRegisterTypes = Depends(authenticate_user)) -> SubjectTypeResponse:
    subjects_collection = await get_subject_collection()
    subjects = subjects_collection.find(
        {"class_name_id": details.class_name_id}).to_list()

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
