from app.services.pdf_parser import PDFParser
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import VectorStore
from app.services.search import SearchService


pdf_parser = PDFParser()
text_chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()

search_service = SearchService(
    embedding_generator,
    vector_store,
)