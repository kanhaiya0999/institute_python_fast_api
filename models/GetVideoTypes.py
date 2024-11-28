from pydantic import BaseModel


class GetVideoTypes(BaseModel):
    video_object_id: str
