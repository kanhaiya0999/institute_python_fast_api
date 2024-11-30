
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from models.UserRegisterTypes import UserRegisterTypes
from models.StatusMessages import StatusMessages
from models.BaseResponse import BaseResponse
from fastapi import Depends
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_user_collection

router = APIRouter()


class UserDetails(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[int]
    id: str


class GetUsersDetailsResponse(BaseResponse):
    users: Optional[list[UserDetails]] = None


@router.get("/api/get_users_details", response_model=GetUsersDetailsResponse)
async def get_users_details(user_details: UserRegisterTypes = Depends(authenticate_user)) -> GetUsersDetailsResponse:

    if user_details.type != 'admin':
        return GetUsersDetailsResponse(
            status=401,
            message=StatusMessages.UNAUTHORIZED.value,
            is_success=False
        )
    user_collection = await get_user_collection()

    all_users = user_collection.find()

    all_users_list = [
        UserDetails(
            name=user.get('name', ''),
            email=user.get('email', ''),
            phone=user.get('phone', ''),
            id=str(user['_id'])
        ) for user in all_users
    ]

    return GetUsersDetailsResponse(
        status=200,
        message=StatusMessages.USERS_FETCHED.value,
        is_success=True,
        users=all_users_list
    )
