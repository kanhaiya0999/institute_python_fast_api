from fastapi import APIRouter, Depends
from models.BaseResponse import BaseResponse
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user

router = APIRouter()


class checkUserResponse(BaseResponse):
    type: str


@router.get("/api/get_check_user")
async def get_check_user(
        user_details: UserRegisterTypes = Depends(authenticate_user)) -> checkUserResponse:
    return checkUserResponse(
        status=200,
        message="User Fetched",
        is_success=True,
        type=user_details.type,
    )
