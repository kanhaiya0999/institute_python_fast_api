from bson import ObjectId
from fastapi import APIRouter, Depends, Request

from models.BaseResponse import BaseResponse
from models.PDFsTypes import PDFsTypes
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_pdf_collection, get_subject_collection


router = APIRouter()


@router.post("/api/add_pdf")
async def add_pdf(details: PDFsTypes, request: Request, user_details: UserRegisterTypes = Depends(authenticate_user)) -> BaseResponse:

    if user_details.type != 'admin':
        return BaseResponse(
            status=401,
            message=StatusMessages.UNAUTHORIZED.value,
            is_success=False
        )
    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.subject_object_id)})
    if subject_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.SUBJECT_NOT_FOUND.value,
            is_success=False

        )

    pdfs_collection = await get_pdf_collection()
    pdfs_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.PDF_ADDED.value,
        is_success=True

    )
