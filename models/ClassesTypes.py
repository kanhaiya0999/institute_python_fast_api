from pydantic import BaseModel


class ClassesTypes(BaseModel):
    name: str
    desc: str
    price: int
