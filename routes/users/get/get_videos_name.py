

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.GetVideoNameTypes import GetVideoNameTypes
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_video_collection

router = APIRouter()


class videoTypes(BaseModel):
    id: str
    name: str


class videoTypesResponse(BaseResponse):
    videos: list[videoTypes]


@router.get("/api/get_videos_name")
async def get_videos_name(details: GetVideoNameTypes, request: Request, user_details: UserRegisterTypes = Depends(authenticate_user)) -> videoTypesResponse:
    videos_collection = await get_video_collection()
    videos = videos_collection.find(
        {"subject_object_id": details.video_object_id}, {"video": False})
    videos = [
        videoTypes(
            id=str(video["_id"]),
            name=video["name"]
        ) for video in videos

    ]
    return videoTypesResponse(
        status=200,
        message="Videos Fetched",
        is_success=True,
        videos=videos


    )
