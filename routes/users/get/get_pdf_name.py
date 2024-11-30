from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_pdf_collection

router = APIRouter()


class pdfListType(BaseModel):
    id: str
    name: str
    subject_object_id: str


class postPdfResponseType(BaseResponse):
    pdfs: List[pdfListType]


@router.get("/api/get_pdfs_name")
async def get_pdfs_name(subject_object_id: str,
                        user_details: UserRegisterTypes = Depends(authenticate_user)) -> postPdfResponseType:

    pdfs_collection = await get_pdf_collection()
    pdfs = pdfs_collection.find(
        {"subject_object_id": subject_object_id}, {"pdf": False}).to_list()
    data = [
        pdfListType(
            id=str(pdf["_id"]),
            name=pdf["name"],
            subject_object_id=pdf["subject_object_id"]
        ) for pdf in pdfs
    ]
    return postPdfResponseType(
        status=200,
        message="PDFs Fetched",
        is_success=True,
        pdfs=data
    )
