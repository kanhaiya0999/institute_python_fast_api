from fastapi import APIRouter, Depends, Request

from models.BaseResponse import BaseResponse
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user

router = APIRouter()


class checkUserResponse(BaseResponse):
    type: str


@router.post("/api/post_check_user")
async def post_check_user(request: Request,
                          user_details: UserRegisterTypes = Depends(authenticate_user)) -> checkUserResponse:
    return checkUserResponse(
        status=200,
        message="User Fetched",
        is_success=True,
        type=user_details.type,
    )
