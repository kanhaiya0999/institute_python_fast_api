from fastapi import File
from pydantic import BaseModel


class VideoTypes(BaseModel):
    subject_object_id: str
    name: str
    video: bytes = File(media_type="video/mp4")
