from bson import ObjectId
from fastapi import APIRouter, Depends

from models.BaseResponse import BaseResponse
from models.ClassesTypes import ClassesTypes
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_admin
from utils.connect_db import get_class_collection

router = APIRouter()


class UpdateClassType(ClassesTypes):
    id: str


@router.post("/api/update_class")
async def update_class(details: UpdateClassType,  user_details: UserRegisterTypes = Depends(authenticate_admin)) -> BaseResponse:

    classes_collection = await get_class_collection()
    classes_collection.update_one({"_id": ObjectId(details.id)}, {
                                  "$set": {"name": details.name, "desc": details.desc, "price": details.price}})
    return BaseResponse(
        status=200,
        message=StatusMessages.CLASS_UPDATED.value,
        is_success=True
    )
