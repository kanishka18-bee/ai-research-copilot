import uuid
import shutil
import logging
import os
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from app.core.config import DOCUMENT_STORAGE, MAX_FILE_SIZE
from app.schemas.document import DocumentUploadResponse
from app.services.pdf_parser import PDFParser

logger = logging.getLogger(__name__)
pdf_parser = PDFParser()


class DocumentService:

    def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        
        # check mime type
        if file.content_type != "application/pdf":
            logger.warning(f"Invalid file type uploaded: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed."
            )

        # validate file type
        header = file.file.read(5)
        file.file.seek(0)  # Reset file pointer to the beginning after reading
        
        if header != b"%PDF-":
            logger.warning(f"Uploaded file is not a valid PDF: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PDF file."
            )
            
        # check file size
        file.file.seek(0, os.SEEK_END)          # Move to end of file
        file_size = file.file.tell()  # Get current position = file size
        file.file.seek(0)             # Move back to beginning
        
        if file_size > MAX_FILE_SIZE:
            logger.warning(
                f"File too large: {file.filename} ({file_size} bytes)"
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Maximum allowed file size is {MAX_FILE_SIZE // (1024 * 1024)} MB."
            )
        
        
        # generate unique document ID 
        document_id = str(uuid.uuid4())
        
        # keep the original filename
        filename = file.filename
        
        # get the file extension (.pdf)
        extension = Path(filename).suffix
        
        # Path to backend/storage/documents
        storage_path = DOCUMENT_STORAGE
        storage_path.mkdir(parents=True, exist_ok=True)  # Ensure the storage directory exists
        
        # create folder if it doesn't exist
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # final filename on disk
        stored_file = storage_path / f"{document_id}{extension}"
        
        # save uploaded PDF
        with open(stored_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # file size in bytes
        size = stored_file.stat().st_size
        
        logger.info(
            f"Document uploaded successfully: {filename} ({size} bytes)"
        )

        parsed_pdf = pdf_parser.parse(stored_file)
        print(parsed_pdf)  # For debugging purposes, you can remove this in production
        
        # return response
        return DocumentUploadResponse(
            id=document_id,
            filename=filename,
            size=size,
            content_type=file.content_type,
            status="uploaded"
        )