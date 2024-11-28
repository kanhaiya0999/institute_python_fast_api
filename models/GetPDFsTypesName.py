from pydantic import BaseModel


class GetPDFsTypesName(BaseModel):
    subject_object_id: str
