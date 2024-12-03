from typing import Optional
from fastapi import File
from pydantic import BaseModel


class VideoTypes(BaseModel):
    subject_object_id: str
    name: str
    video: bytes | None = File("video/mp4")
    video_object_id: Optional[str] = None
