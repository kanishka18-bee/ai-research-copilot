import logging

from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import (
    VectorStore,
    SearchResult,
)

logger = logging.getLogger(__name__)


class SearchService:
    """
    Performs semantic search over indexed document chunks.
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[SearchResult]:

        if not query or not query.strip():
            logger.warning("Search query is empty.")
            return []

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        logger.info(
            "Searching for query: %s (top_k=%d)",
            query,
            top_k,
        )

        query_embedding = self.embedding_generator.embed([query])

        results = self.vector_store.search(
            query_embedding,
            top_k,
        )

        logger.info(
            "Retrieved %d matching chunks.",
            len(results),
        )

        return results