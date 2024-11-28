import fastapi

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.connect_db import get_user_collection


router = fastapi.APIRouter()


@router.post("/api/register")
async def register_user(details: UserRegisterTypes) -> BaseResponse:

    users_collection = await get_user_collection()
    user_details = users_collection.find_one({"email": details.email})
    if user_details is not None:
        return BaseResponse(
            status=400,
            message=StatusMessages.USER_ALREADY_EXISTS.value,
            is_success=False
        )

    users_collection.insert_one(details.model_dump())
    return BaseResponse(
        status=200,
        message=StatusMessages.USER_CREATED.value,
        is_success=True

    )
