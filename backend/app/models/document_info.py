from dataclasses import dataclass

@dataclass
class DocumentInfo:
    """
    Represents a single uploaded document.
    """
    
    document_id: str
    filename:  str
    chunk_count: int