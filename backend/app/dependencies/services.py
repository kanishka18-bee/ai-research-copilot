from app.services.pdf_parser import PDFParser
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import VectorStore
from app.services.search import SearchService
from app.services.prompt_builder import PromptBuilder
from app.services.llm import LLMService
from app.services.chat import ChatService


pdf_parser = PDFParser()
text_chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()
vector_store.load()  # Load existing embeddings and chunks from storage

search_service = SearchService(
    embedding_generator,
    vector_store,
)

prompt_builder = PromptBuilder()

llm_service = LLMService()

chat_service = ChatService(
    search_service,
    prompt_builder,
    llm_service,
)