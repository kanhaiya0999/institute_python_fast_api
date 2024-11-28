from pydantic import BaseModel, Field


class SubjectsTypes(BaseModel):
    class_name_id: str = Field(max_length=24, min_length=24)
    name: str
