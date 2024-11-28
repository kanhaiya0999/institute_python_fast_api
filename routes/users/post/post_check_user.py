from typing import List
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user

router = APIRouter()


class pdfListType(BaseModel):
    id: str
    name: str
    subject_object_id: str


class getPdfResponseType(BaseResponse):
    pdfs: List[pdfListType]


@router.post("/api/post_check_user")
async def post_check_user(request: Request,
                          user_details: UserRegisterTypes = Depends(authenticate_user)) -> BaseResponse:
    return BaseResponse(
        status=200,
        message="User Fetched",
        is_success=True
    )
