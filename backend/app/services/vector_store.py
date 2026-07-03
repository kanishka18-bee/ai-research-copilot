import logging
import numpy as np
import faiss

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Stores and retrieves text embeddings using a FAISS index.
    """
    
    def __init__(self):
        self.dimension = 384

        self.index = faiss.IndexFlatIP(self.dimension)

        self.chunks: list[str] = []

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

        logger.info(
            "Added %d embeddings to FAISS.",
            len(chunks),
        )

    @property
    def size(self) -> int:
        return self.index.ntotal

    def save(self):
        pass

    def load(self):
        pass

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[str]:

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

        logger.info(
            "Searching FAISS index (top_k=%d).",
            top_k,
        )

        _, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results: list[str] = []

        for index in indices[0]:
            if index == -1:
                continue

            results.append(self.chunks[index])

        logger.info(
            "Retrieved %d matching chunks.",
            len(results),
        )

        return results
