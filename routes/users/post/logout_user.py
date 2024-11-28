from fastapi import APIRouter, Request, Response

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from utils.connect_db import get_user_collection


router = APIRouter()


@router.post("/api/logout")
async def logout_user(request: Request, response: Response) -> BaseResponse:
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return BaseResponse(
            status=401,
            message=StatusMessages.UNAUTHORIZED.value,
            is_success=False

        )
    user_collection = await get_user_collection()
    user_details = user_collection.find_one({"jwt": user_jwt})
    if user_details is None:
        return BaseResponse(
            status=404,
            message=StatusMessages.USER_NOT_FOUND.value,
            is_success=False

        )

    user_collection.update_one({"jwt": user_jwt}, {
        "$set": {"jwt": None, "jwt_expire": None}})
    return BaseResponse(
        status=200,
        message=StatusMessages.USER_LOGOUT.value,
        is_success=True

    )
