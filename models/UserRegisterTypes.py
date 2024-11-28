from pydantic import BaseModel, EmailStr


class UserRegisterTypes(BaseModel):
    name: str
    email: EmailStr
    phone: int
    password: str
    type: str = "user"
    jwt: str | None = None
    jwt_expire: str | None = None
