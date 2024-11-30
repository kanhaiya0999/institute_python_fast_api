from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models.BaseResponse import BaseResponse
from models.StatusMessages import StatusMessages
from models.UserRegisterTypes import UserRegisterTypes
from utils.authenticate_user import authenticate_user
from utils.connect_db import get_class_collection


router = APIRouter()


class ClassResponse(BaseModel):
    id: str
    name: str
    desc: str
    price: int


class ClassTypeResponse(BaseResponse):
    classes: List[ClassResponse]


@router.get("/api/get_classes")
async def get_classes(user_details: UserRegisterTypes = Depends(authenticate_user)) -> ClassTypeResponse:
    classes_collection = await get_class_collection()
    classes = classes_collection.find().to_list()
    data = [
        ClassResponse(
            id=str(class_["_id"]),
            name=class_["name"],
            desc=class_["desc"],
            price=class_["price"]
        ) for class_ in classes
    ]
    return ClassTypeResponse(
        status=200,
        message=StatusMessages.CLASS_FETCHED.value,
        is_success=True,
        classes=data
    )
