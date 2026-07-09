from fastapi import (
    APIRouter, 
    UploadFile, 
    File,
    Path,
)

from app.schemas.document import (
    DocumentUploadResponse,
    DocumentInfoResponse,
)

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

@router.get(
    "",
    response_model=list[DocumentInfoResponse],
)

def list_documents() -> list[DocumentInfoResponse]:
    """ 
    Returns all uploaded documents with their information.
    """
    
    documents = document_service.list_documents()
    
    return [
        DocumentInfoResponse(
            document_id=document.document_id,
            filename=document.filename,
            chunk_count=document.chunk_count,
        )
        for document in documents
    ]

@router.delete(
    "/{document_id}",
    status_code=204,
)
def delete_document(
    document_id: str = Path(
        ...,
        description="The ID of the document to delete.",
    ),
) -> None:
    """ 
    Deletes an uploaded document and its associated chunks from the vector store.
    """
    
    document_service.delete_document(
        document_id,
    )