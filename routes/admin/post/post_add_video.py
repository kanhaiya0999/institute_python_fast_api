from bson import ObjectId
from fastapi import APIRouter, Depends
from gridfs import GridFS

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from models.VideoTypes import VideoTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_db, get_subject_collection, get_video_collection

router = APIRouter()


@router.post("/api/add_video")
async def add_video(details: VideoTypes,  user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:

    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.subject_object_id)})
    if subject_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.SUBJECT_NOT_FOUND.value,
            is_success=False


        )
    videos_collection = await get_video_collection()
    db = await get_db()
    fs = GridFS(db)
    file_id = fs.put(details.video, filename=details.name)
    details.video = file_id
    details.subject_object_id = subject_details["_id"]
    details.video_object_id = file_id
    details.video = None
    videos_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.VIDEO_ADDED.value,
        is_success=True
    )
