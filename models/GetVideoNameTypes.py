from pydantic import BaseModel


class GetVideoNameTypes(BaseModel):
    video_object_id: str
