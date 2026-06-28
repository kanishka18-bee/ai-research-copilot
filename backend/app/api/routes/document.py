from fastapi import APIRouter, UploadFile, File

from app.schemas.document import DocumentUploadResponse
from app.services.document import DocumentService

router = APIRouter()

document_service = DocumentService()

@router.post(
    "/upload",
    response_model=DocumentUploadResponse
)

def upload_document(
    file: UploadFile = File(...)
) -> DocumentUploadResponse:
    
    return document_service.upload_document(file)