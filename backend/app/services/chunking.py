import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Splits extracted PDF text into overlapping chunks for downstream
    embedding generation and semantic search.
    """

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size.")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Extracted text from the PDF.

        Returns:
            List of text chunks.
        """

        if not text or not text.strip():
            logger.warning("Input text is empty.")
            return []

        logger.info(
            "Splitting text into chunks (%d characters).",
            len(text)
        )

        chunks: list[str] = []
        
        start = 0
        text_length = len(text)
        
        while start < text_length:
            
            end = min(start + self.chunk_size, text_length)
            
            # Move end back to the nearest word or paragraph boundary
            if end < text_length:
                last_break = max(
                    text.rfind(" ", start, end),
                    text.rfind("\n", start, end),
                )
                
                if last_break > start + self.chunk_size // 2: 
                    end = last_break
                    
            chunk = text[start:end].strip()
            
            if chunk:
                chunks.append(chunk)
                
            # Finished processing the document
            if end >= text_length:
                break
            
            # Start next chunk with overlap
            start = max(0, end - self.overlap)
            
            
            # Move start forward to the next whitespace so we don't begin in the middle of a word
            while start < text_length and not text[start].isspace():
                start += 1 
                
            while start < text_length and text[start].isspace():
                start += 1
        
        logger.info(
            "Created %d chunks.",
            len(chunks)
        )

        return chunks