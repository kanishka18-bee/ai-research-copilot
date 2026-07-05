import logging
import numpy as np
import faiss
import json


from app.core.config import (
    SIMILARITY_THRESHOLD,
    EMBEDDING_STORAGE,
)

from dataclasses import dataclass

logger = logging.getLogger(__name__)



@dataclass
class SearchResult:
    """
    Represents a semantic search result 
    returned by the vector store.
    """
    score: float
    chunk: str
    index: int


class VectorStore:
    """
    Stores and retrieves text embeddings 
    using a FAISS index.
    """
    
    def __init__(self):
        self.dimension = 384

        self.index = faiss.IndexFlatIP(self.dimension)

        self.chunks: list[str] = []
        
        self.storage_path = EMBEDDING_STORAGE
        
        self.index_file = self.storage_path / "index.faiss"
        
        self.chunks_file = self.storage_path / "chunks.json"
        
        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )
        

        logger.info("FAISS vector store initialized.")


    def add_embeddings(self, chunks: list[str], embeddings: np.ndarray) -> None:

        if not chunks:
            logger.warning("No chunks to add.")
            return

        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have the same length.")

        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Expected embeddings of dimension {self.dimension}, "
                f"got {embeddings.shape[1]}."
            )

        self.index.add(embeddings)

        self.chunks.extend(chunks)
        
        self.save()
    
        logger.info(
            "Added %d embeddings to FAISS.",
            len(chunks),
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
                self.chunks_file, 
                "w",
                encoding="utf-8",
            ) as file:
            
                json.dump(
                    self.chunks, 
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
            chunks_exist = self.chunks_file.exists()
            
            if not index_exists and not chunks_exist:
                logger.info(
                    "No existing vector store found. Starting with an empty index."    
                )
                return
            
            if index_exists != chunks_exist:
                raise RuntimeError(
                    "Vector store is incomplete. Both index.faiss and chunks.json are required."
                )
            
            self.index = faiss.read_index(
                self.index_file.as_posix()
            )
            
            with open(
                self.chunks_file,
                "r",
                encoding="utf-8",
            ) as file:
                
                self.chunks = json.load(file)
            
            if self.index.ntotal != len(self.chunks):
                raise RuntimeError(
                    "Vector store is inconsistent: embedding count does not match chunk count."
                )
                
            logger.info(
                "Loaded %d vectors and %d chunks from storage.",
                self.index.ntotal,
                len(self.chunks),
            )
            
        except Exception:
            logger.exception(
                "Failed to load vector store."
            )
            raise
            

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
                    chunk=self.chunks[index],
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
            "Retrieved %d matching chunks.",
            len(results),
        )

        return results
