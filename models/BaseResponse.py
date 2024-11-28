from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int
    message: str
    is_success: bool
