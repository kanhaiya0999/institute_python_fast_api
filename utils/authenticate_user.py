
from utils.connect_db import get_user_collection
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes

from fastapi import HTTPException, Header
import datetime


async def authenticate_user(x_auth_token: str = Header(...)):
    user_jwt = x_auth_token

    if not user_jwt:
        raise HTTPException(
            status_code=401, detail=StatusMessages.UNAUTHORIZED.value
        )

    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)

    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}}
    )

    if not user_details:
        raise HTTPException(
            status_code=404, detail=StatusMessages.USER_NOT_FOUND.value
        )

    return UserRegisterTypes(
        name=user_details['name'],
        email=user_details['email'],
        phone=user_details['phone'],
        password=user_details['password'],
        type=user_details['type'],

    )
