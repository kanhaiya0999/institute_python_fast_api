from pydantic import BaseModel, EmailStr


class UserLoginTypes(BaseModel):
    email: EmailStr
    password: str
