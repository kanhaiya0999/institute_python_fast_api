from bson import ObjectId
from fastapi import APIRouter, Depends
from gridfs import GridFS

from models.BaseResponse import BaseResponse
from models.PDFsTypes import PDFsTypes
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_db, get_pdf_collection, get_subject_collection


router = APIRouter()


@router.post("/api/add_pdf")
async def add_pdf(details: PDFsTypes, user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:
    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.subject_object_id)})
    if subject_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.SUBJECT_NOT_FOUND.value,
            is_success=False

        )
    db = await get_db()
    fs = GridFS(db)
    file_id = fs.put(details.pdf, filename=details.name)
    print(file_id)
    details.pdf_object_id = file_id
    details.subject_object_id = subject_details["_id"]
    details.pdf = None
    # details.subject_object_id = subject_details["_id"]
    pdfs_collection = await get_pdf_collection()

    pdfs_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.PDF_ADDED.value,
        is_success=True

    )
