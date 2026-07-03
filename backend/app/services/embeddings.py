import logging
import numpy as np

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    # generates text embeddings from text chunks
      
    def __init__(self):
        logger.info("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedding model loaded successfully.")
        

    def embed(self, chunks: list[str]) -> np.ndarray:
        # generate embeddings for a lisy of text chunks
        
        if not chunks:
            logger.warning("No chunks provided for embedding.")
            dimension = self.model.get_embedding_dimension()
            
            return np.empty(
                (0, dimension),
                dtype=np.float32
            )
        
        logger.info("Generating embeddings for %d chunks.", len(chunks))
        
        embeddings: np.ndarray = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        
        logger.info(
            "Generated embeddings for %d chunks.", 
            len(embeddings)
        )
        
        return embeddings.astype(np.float32, copy=False)
    
