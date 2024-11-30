

from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, Header

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_video_collection

router = APIRouter()


class videoType(BaseResponse):
    id:  Optional[str] = None
    name:  Optional[str] = None
    video:  Optional[bytes] = None


@router.get("/api/get_video")
async def get_video(video_object_id: str, x_auth_token: str = Header(...),  user_details: UserRegisterTypes = Depends(authenticate_user)) -> videoType:

    videos_collection = await get_video_collection()
    video_details = videos_collection.find_one(
        {"_id": ObjectId(video_object_id)})
    if video_details is None:
        return videoType(
            status=404,
            message=StatusMessages.VIDEO_NOT_FOUND.value,
            is_success=False
        )

    video_details = dict(video_details, _id=str(video_details["_id"]))
    return videoType(
        id=str(video_details["_id"]),
        name=video_details["name"],
        video=video_details["video"],
        is_success=True,
        status=200,
        message=StatusMessages.VIDEO_FETCHED.value
    )
