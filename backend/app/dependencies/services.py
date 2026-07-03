from app.services.pdf_parser import PDFParser
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import VectorStore


pdf_parser = PDFParser()
text_chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()