
from typing import Optional
from fastapi import File
from pydantic import BaseModel


class PDFsTypes(BaseModel):
    subject_object_id: str
    name: str
    pdf: bytes | None = File("application/pdf")
    pdf_object_id: Optional[str] = None
