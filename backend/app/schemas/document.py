from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    size: int
    content_type: str
    status: str
    
class DocumentInfoResponse(BaseModel):
    """ 
    Information about an uploaded document.
    """
    
    document_id: str
    filename: str
    chunk_count: int
    
