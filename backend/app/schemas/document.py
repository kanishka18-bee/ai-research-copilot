from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    size: int
    content_type: str
    status: str
