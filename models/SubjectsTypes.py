from pydantic import BaseModel


class SubjectsTypes(BaseModel):
    class_object_id: str
    name: str
