from pydantic import BaseModel


class GetPdfFileType(BaseModel):
    pdf_object_id: str
