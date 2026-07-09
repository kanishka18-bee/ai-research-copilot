import uuid
import shutil
import logging
import os
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from app.core.config import DOCUMENT_STORAGE, MAX_FILE_SIZE
from app.schemas.document import DocumentUploadResponse
from app.models.document_info import DocumentInfo

from app.models.metadata import ChunkMetadata

from app.dependencies.services import (
    pdf_parser,
    text_chunker,
    embedding_generator,
    vector_store,
)

logger = logging.getLogger(__name__)


class DocumentService:
    """
    Handles document upload, processing, and indexing.
    """

    def upload_document(self, file: UploadFile) -> DocumentUploadResponse:

        # check mime type
        if file.content_type != "application/pdf":
            logger.warning("Invalid file type uploaded: %s", file.content_type)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed.",
            )

        # validate file type
        header = file.file.read(5)
        file.file.seek(0)  # Reset file pointer to the beginning after reading

        if header != b"%PDF-":
            logger.warning(
                "Uploaded file is not a valid PDF: %s",
                file.filename,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PDF file."
            )

        # check file size
        file.file.seek(0, os.SEEK_END)  # Move to end of file
        file_size = file.file.tell()  # Get current position = file size
        file.file.seek(0)  # Move back to beginning

        if file_size > MAX_FILE_SIZE:
            logger.warning(
                "File too large: %s (%d bytes)",
                file.filename,
                file_size,
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Maximum allowed file size is {MAX_FILE_SIZE // (1024 * 1024)} MB.",
            )

        # generate unique document ID
        document_id = str(uuid.uuid4())

        # keep the original filename
        filename = file.filename

        # get the file extension (.pdf)
        extension = Path(filename).suffix

        # Path to backend/storage/documents
        storage_path = DOCUMENT_STORAGE
        storage_path.mkdir(
            parents=True, exist_ok=True
        )  # Ensure the storage directory exists

        # final filename on disk
        stored_file = storage_path / f"{document_id}{extension}"

        # save uploaded PDF
        with open(stored_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # file size in bytes
        size = stored_file.stat().st_size

        logger.info(
            "Document uploaded successfully: %s (%d bytes).",
            filename,
            size,
        )

        parsed_pdf = pdf_parser.parse(stored_file)

        text = parsed_pdf["text"]

        chunks = text_chunker.split_text(text)

        chunk_metadata = [
            ChunkMetadata(
                chunk=chunk,
                document_id=document_id,
                filename=filename,
                page_number=None,
            )
            for chunk in chunks
        ]

        chunk_texts = [metadata.chunk for metadata in chunk_metadata]

        embeddings = embedding_generator.embed(chunk_texts)

        if len(embeddings) != len(chunk_metadata):
            raise RuntimeError(
                "Embedding generation returned an unexpected number of vectors."
            )

        vector_store.add_embeddings(
            chunk_metadata,
            embeddings,
        )

        logger.info(
            "Indexed %d chunk metadata records for document '%s'. Vector store size: %d.",
            len(chunk_metadata),
            filename,
            vector_store.size,
        )

        # return response
        return DocumentUploadResponse(
            id=document_id,
            filename=filename,
            size=size,
            content_type=file.content_type,
            status="uploaded",
        )
        
    def list_documents(
        self,
    ) -> list[DocumentInfo]:
        """ 
        Returns information about all uploaded documents.
        """
        
        logger.info(
            "Retrieving uploaded documents."
        )
        
        return vector_store.list_documents()

    def delete_document(
        self, 
        document_id: str,
    ) ->  None:
        """ 
        Deletes an uploaded document and its associated chunks from the vector store.
        """
        
        document = next(
            (
                metadata 
                for metadata in vector_store.chunk_metadata
                if metadata.document_id == document_id
            ),
            None
        )
        
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )   
            
        stored_file = DOCUMENT_STORAGE / f"{document_id}.pdf"
        
        if stored_file.exists():
            stored_file.unlink()
            
            logger.info(
                "Deleted stored file for document '%s'.",
                document.filename
            )
            
        vector_store.delete_document(
            document_id,
            embedding_generator,
        )   
        
        logger.info(
            "Document '%s' deleted successfully.",
            document.filename,
        ) 