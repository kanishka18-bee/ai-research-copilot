import logging
import numpy as np
import faiss
import json


from app.core.config import (
    SIMILARITY_THRESHOLD,
    EMBEDDING_STORAGE,
)

from app.models.metadata import ChunkMetadata
from app.models.document_info import DocumentInfo
from app.services.embeddings import EmbeddingGenerator

from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)



@dataclass
class SearchResult:
    """
    Represents a semantic search result 
    returned by the vector store.
    """
    score: float
    metadata: ChunkMetadata
    index: int


class VectorStore:
    """
    Stores and retrieves text embeddings 
    using a FAISS index.
    """
    
    def __init__(self):
        self.dimension = 384

        self.index = faiss.IndexFlatIP(self.dimension)

        self.chunk_metadata: list[ChunkMetadata] = []
        
        self.storage_path = EMBEDDING_STORAGE
        
        self.index_file = self.storage_path / "index.faiss"
        
        self.metadata_file = self.storage_path / "metadata.json"
        
        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )
        

        logger.info("FAISS vector store initialized.")


    def add_embeddings(
        self, 
        metadata: list[ChunkMetadata], 
        embeddings: np.ndarray
    ) -> None:

        if not metadata:
            logger.warning("No metadata to add.")
            return

        if len(metadata) != len(embeddings):
            raise ValueError("Metadata and embeddings must have the same length.")

        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Expected embeddings of dimension {self.dimension}, "
                f"got {embeddings.shape[1]}."
            )

        self.index.add(embeddings)

        self.chunk_metadata.extend(metadata)
        
        self.save()
    
        logger.info(
            "Added %d embeddings to FAISS.",
            len(metadata),
        )

    @property
    def size(self) -> int:
        """
        Returns the number of indexed vectors.
        """
        return self.index.ntotal

    def save(self):
        
        try:
            faiss.write_index(
                self.index, 
                self.index_file.as_posix(),
            )

            with open(
                self.metadata_file, 
                "w",
                encoding="utf-8",
            ) as file:
            
                json.dump(
                    [asdict(metadata) for metadata in self.chunk_metadata],
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
            
            logger.info(
                "Vector store saved successfully."
            )
                
        except Exception:
            logger.exception(
                "Failed to save vector store."
            )
            raise

    def load(self) -> None:
        
        try:
            
            index_exists = self.index_file.exists()
            metadata_exists = self.metadata_file.exists()
            
            if not index_exists and not metadata_exists:
                logger.info(
                    "No existing vector store found. Starting with an empty index."    
                )
                return
            
            if index_exists != metadata_exists:
                raise RuntimeError(
                    "Vector store is incomplete. Both index.faiss and metadata.json are required."
                )
            
            self.index = faiss.read_index(
                self.index_file.as_posix()
            )
            
            with open(
                self.metadata_file,
                "r",
                encoding="utf-8",
            ) as file:
                
                content = file.read().strip()
                
                if not content:
                    logger.warning(
                        "Metadata file is empty. Starting with an empty vector store."
                    )
                    
                    self.chunk_metadata = []
                    return
                
                loaded_metadata = json.loads(content)
                
                self.chunk_metadata = [
                    ChunkMetadata(**metadata)
                    for metadata in loaded_metadata
                ]
            
            if self.index.ntotal != len(self.chunk_metadata):
                raise RuntimeError(
                    "Vector store is inconsistent: embedding count does not match chunk count."
                )
                
            logger.info(
                "Loaded %d vectors and %d chunk metadata records.",
                self.index.ntotal,
                len(self.chunk_metadata),
            )
            
        except Exception:
            logger.exception(
                "Failed to load vector store."
            )
            raise
          
    def list_documents(self) -> list[DocumentInfo]:
        """
        Returns a list of uploaded documents.
        """
        documents: dict[str, DocumentInfo] = {}
        
        for metadata in self.chunk_metadata:
            document_id = metadata.document_id
            
            if document_id not in documents:
                documents[document_id] = DocumentInfo(
                    document_id=document_id,
                    filename=metadata.filename,
                    chunk_count=1,
                )
            else:
                documents[document_id].chunk_count += 1

        logger.info(
            "Retrieved %d unique documents from chunk metadata.",
            len(documents),
        )

        return list(documents.values())

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[SearchResult]:

        if self.size == 0:
            logger.warning("FAISS index is empty.")
            return []

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        query_embedding = np.atleast_2d(query_embedding).astype(np.float32)

        if query_embedding.shape[1] != self.dimension:
            raise ValueError(
                f"Expected embedding dimension {self.dimension}, "
                f"got {query_embedding.shape[1]}."
            )

        top_k = min(top_k, self.size)

        logger.info(
            "Searching FAISS index (top_k=%d).",
            top_k,
        )
        
        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results: list[SearchResult] = []

        for i, index in enumerate(indices[0]):
            if index == -1:
                continue
            
            score = float(distances[0][i])
            
            if score < SIMILARITY_THRESHOLD:
                continue

            results.append(
                SearchResult(
                    score=score,
                    metadata=self.chunk_metadata[index],
                    index=index
                )
            )

        if not results:
            logger.info(
                "No search results met the similarity threshold (%.2f).",
                SIMILARITY_THRESHOLD,
            )
        
        else:
            logger.info(
                "Top similarity score: %.4f",
                results[0].score,
            )

        logger.info(
            "Retrieved %d matching chunk metadata records.",
            len(results),
        )

        return results
    
    def delete_document(
        self,
        document_id: str,
        embedding_generator: EmbeddingGenerator,
    ) -> None:
        """
        Removes all chunk metadata and embeddings associated with a document,
        rebuilds the FAISS index, and persists the updated vector store.
        """
        
        logger.info(
            "Deleting document '%s' from vector store.",
            document_id
        )
        
        remaining_metadata = [
            metadata
            for metadata in self.chunk_metadata
            if metadata.document_id != document_id
        ]
        
        deleted_count = len(self.chunk_metadata) - len(remaining_metadata)

        if deleted_count == 0:
            raise ValueError(
                f"Document '{document_id}' not found in vector store."
            )
            
        if not remaining_metadata:
            
            self.index = faiss.IndexFlatIP(self.dimension)
            self.chunk_metadata = []
            self.save()
            
            logger.info(
                "Deleted document '%s'. Vector store is now empty.",
                document_id
            )
            
            return
        
        remaining_chunks = [
            metadata.chunk
            for metadata in remaining_metadata
        ]
            
        embeddings = embedding_generator.embed(
            remaining_chunks
        )
            
        if len(embeddings) != len(remaining_metadata):
            raise RuntimeError(
                "Embedding generation returned an unexpected number of vectors."
            )
        
        self.index = faiss.IndexFlatIP(
            self.dimension
        )
            
        self.index.add(embeddings)
            
        self.chunk_metadata = remaining_metadata
            
        self.save()
            
        logger.info(
            "Deleted document '%s' and rebuilt the vector store with %d remaining chunks.",
            document_id,
            len(remaining_metadata)
        )