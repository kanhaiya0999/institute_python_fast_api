from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Depends

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_pdf_collection

router = APIRouter()


class pdfResponseType(BaseResponse):
    id: Optional[str] = None
    subject_object_id:  Optional[str] = None
    name:  Optional[str] = None
    pdf:  Optional[bytes] = None


@router.get("/api/get_pdf")
async def get_pdf(pdf_object_id: str,  user_details: UserRegisterTypes = Depends(authenticate_user)) -> pdfResponseType:
    pdfs_collection = await get_pdf_collection()
    pdf_details = pdfs_collection.find_one(
        {"_id": ObjectId(pdf_object_id)})
    if pdf_details is None:
        return pdfResponseType(status=404, message=StatusMessages.PDF_NOT_FOUND.value, is_success=False)

    pdf_details = dict(pdf_details, _id=str(pdf_details["_id"]))
    return pdfResponseType(
        id=str(pdf_details["_id"]),
        subject_object_id=pdf_details["subject_object_id"],
        name=pdf_details["name"],
        pdf=pdf_details["pdf"],
        is_success=True,
        status=200,
        message=StatusMessages.PDF_FETCHED.value

    )
