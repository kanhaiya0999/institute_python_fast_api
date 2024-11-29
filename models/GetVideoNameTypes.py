from pydantic import BaseModel


class GetVideoNameTypes(BaseModel):
    subject_object_id: str
