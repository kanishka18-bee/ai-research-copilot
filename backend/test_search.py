from pathlib import Path

from app.dependencies.services import (
    pdf_parser,
    text_chunker,
    embedding_generator,
    vector_store,
    search_service,
)

from app.models.metadata import ChunkMetadata

pdf_path = Path(
    r"C:\Users\kanis\OneDrive\Desktop\ai-research-copilot\backend\storage\documents\kanishka-kashyap-resume1.pdf"
)

parsed_pdf = pdf_parser.parse(pdf_path)
text = parsed_pdf["text"]

chunks = text_chunker.split_text(text)

chunk_metadata = [
    ChunkMetadata(
        chunk=chunk,
        document_id="test-document",
        filename=pdf_path.name,
        page_number=None,
    )
    for chunk in chunks
]

chunk_texts = [
    metadata.chunk
    for metadata in chunk_metadata
]
# Check whether the contribution section exists in the chunks

embeddings = embedding_generator.embed(
    chunk_texts
)

vector_store.add_embeddings(
    chunk_metadata,
    embeddings,
)

query = "What programming languages does candidate know?"

results = search_service.search(query)

print("\nTop Results:\n")

for i, result in enumerate(results, start=1):
    print(f"Result {i}")
    print(f"Chunk Index: {result.index}")   
    print(f"Score: {result.score:.4f}")
    print(f"Document: {result.metadata.filename}")
    print(f"Document ID: {result.metadata.document_id}")
    print(f"Page: {result.metadata.page_number}")
    print(result.metadata.chunk[:500])
    print()