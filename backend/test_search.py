from pathlib import Path

from app.dependencies.services import (
    pdf_parser,
    text_chunker,
    embedding_generator,
    vector_store,
    search_service,
)

pdf_path = Path(
    r"C:\Users\kanis\OneDrive\Desktop\ai-research-copilot\backend\storage\documents\3651781.3651800.pdf"
)

parsed_pdf = pdf_parser.parse(pdf_path)
text = parsed_pdf["text"]

chunks = text_chunker.split_text(text)

# Check whether the contribution section exists in the chunks

embeddings = embedding_generator.embed(chunks)

vector_store.add_embeddings(
    chunks,
    embeddings,
)

query = "SparseGraphSage contributions"

results = search_service.search(query)

print("\nTop Results:\n")

for i, result in enumerate(results, start=1):
    print(f"Result {i}")
    print(f"Chunk Index: {result.index}")   # <-- after we add index
    print(f"Score: {result.score:.4f}")
    print(result.chunk[:500])
    print()