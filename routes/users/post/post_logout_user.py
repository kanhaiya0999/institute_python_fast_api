from fastapi import APIRouter, Depends, Header

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_user_collection


router = APIRouter()


@router.post("/api/logout")
async def logout_user(x_auth_token: str = Header(...), user_details: UserRegisterTypes = Depends(authenticate_user)) -> BaseResponse:
    user_collection = await get_user_collection()
    user_collection.update_one({"jwt": x_auth_token}, {
        "$set": {"jwt": None, "jwt_expire": None}})
    return BaseResponse(
        status=200,
        message=StatusMessages.USER_LOGOUT.value,
        is_success=True

    )
