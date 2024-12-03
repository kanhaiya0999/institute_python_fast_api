from bson import ObjectId
from fastapi import APIRouter, Depends
from gridfs import GridFS
from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_class_collection, get_db, get_pdf_collection, get_subject_collection, get_video_collection

router = APIRouter()


@router.delete("/api/delete_class")
async def delete_class(id: str, user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:
    class_collection = await get_class_collection()
    subject_collection = await get_subject_collection()
    pdf_collection = await get_pdf_collection()
    video_collection = await get_video_collection()
    classes = class_collection.find_one({"_id": ObjectId(id)})
    if classes is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.CLASS_NOT_FOUND.value,
            is_success=False
        )

    subjects = subject_collection.find(
        {"class_object_id": id}).to_list()
    subject_collection.delete_many({"class_object_id":  ObjectId(id)})
    class_collection.delete_one({"_id": ObjectId(id)})
    pdfs = pdf_collection.find(
        {"subject_object_id": {"$in": subjects}}).to_list()
    videos = video_collection.find(
        {"subject_object_id": {"$in": subjects}}).to_list()

    pdf_collection.delete_many(
        {"subject_object_id": {"$in": [ObjectId(subject["_id"]) for subject in subjects]}})
    video_collection.delete_many(
        {"subject_object_id": {"$in": [ObjectId(subject["_id"]) for subject in subjects]}})
    db = await get_db()
    fs = GridFS(db)
    fs.delete(
        {"_id": {"$in": [ObjectId(pdf["_id"]) for pdf in pdfs]}}
    )
    fs.delete(
        {"_id": {"$in": [ObjectId(video["_id"]) for video in videos]}}
    )
    return BaseResponse(
        status=200,
        message=StatusMessages.CLASS_DELETED.value,
        is_success=True
    )
