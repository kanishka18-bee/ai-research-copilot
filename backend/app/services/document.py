import uuid
import shutil
from pathlib import Path

from fastapi import UploadFile

from app.schemas.document import DocumentUploadResponse


class DocumentService:

    def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        
        # validate file type
        if file.content_type != "application/pdf":
            raise ValueError("Only PDF files are allowed.")
        
        # generate unique document ID 
        document_id = str(uuid.uuid4())
        
        # keep the original filename
        filename = file.filename
        
        # get the file extension (.pdf)
        extension = Path(filename).suffix
        
        # Path to backend/storage/documents
        storage_path = Path(__file__).parent.parent.parent / "storage" / "documents"
        
        # create folder if it doesn't exist
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # final filename on disk
        stored_file = storage_path / f"{document_id}{extension}"
        
        # save uploaded PDF
        with open(stored_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # file size in bytes
        size = stored_file.stat().st_size
        
        # return response
        return DocumentUploadResponse(
            id=document_id,
            filename=filename,
            size=size,
            content_type=file.content_type,
            status="uploaded"
        )