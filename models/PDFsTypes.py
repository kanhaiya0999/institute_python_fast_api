from fastapi import File
from pydantic import BaseModel


class PDFsTypes(BaseModel):
    subject_object_id: str
    name: str
    pdf: bytes = File(media_type="application/pdf")
