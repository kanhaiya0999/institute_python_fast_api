

from bson import ObjectId
from fastapi import APIRouter, Depends

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_pdf_collection, get_subject_collection, get_video_collection


router = APIRouter()


@router.delete("/api/delete_subject")
async def delete_subject(id: str, user_details: UserRegisterTypes = Depends(authenticate_admin)):
    subject_collection = await get_subject_collection()
    pdf_collection = await get_pdf_collection()
    video_collection = await get_video_collection()
    subject_collection.delete_one({"_id": ObjectId(id)})
    pdf_collection.delete_many(
        {"subject_object_id":  id})
    video_collection.delete_many(
        {"subject_object_id":  id})
    return BaseResponse(status=200, message=StatusMessages.SUBJECT_DELETED.value, is_success=True)
