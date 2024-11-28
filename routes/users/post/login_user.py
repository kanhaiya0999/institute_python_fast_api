import random
from typing import Optional
import fastapi
from fastapi import Response
import jwt

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserLoginTypes import UserLoginTypes
from utils.connect_db import get_user_collection
import datetime

router = fastapi.APIRouter()


class LoginResponse(BaseResponse):
    jwt: Optional[str]


@router.post("/api/login")
async def login_user(details: UserLoginTypes, response: Response) -> LoginResponse:
    from app import KEY

    users_collection = await get_user_collection()
    user_details = users_collection.find_one({"email": details.email})

    if (user_details is None or user_details["password"] != details.password):
        return LoginResponse(
            status=404,
            message=StatusMessages.USER_NOT_FOUND.value,
            is_success=False,
            jwt=""
        )
    current_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = current_time + \
        datetime.timedelta(hours=1)

    jwt_details = {
        "email": user_details["email"],
        "random": random.random(),
        "time": current_time.timestamp(),
        "exp": expiry_time
    }

    encoded_jwt = jwt.encode(jwt_details, KEY, algorithm="HS256")
    user_details["jwt"] = encoded_jwt
    user_details["jwt_expire"] = expiry_time
    users_collection.update_one({"email": details.email}, {
                                "$set": {"jwt": encoded_jwt, "jwt_expire": expiry_time}})
    return LoginResponse(
        status=200,
        message=StatusMessages.USER_LOGIN.value,
        is_success=True,
        jwt=encoded_jwt
    )
