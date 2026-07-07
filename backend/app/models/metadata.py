from dataclasses import dataclass

@dataclass
class ChunkMetadata:
    """
    Stores metadata for a document chunk.
    """
    chunk: str
    document_id: str
    filename: str
    page_number: int | None = None