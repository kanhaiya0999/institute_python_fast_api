from pydantic import BaseModel


class GetSubjectsTypes(BaseModel):
    class_name_id: str
