from pathlib import Path
from pypdf import PdfReader

class PDFParser:
    
    def parse(self, file_path: Path) -> dict:
        reader = PdfReader(file_path)
        
        return{
            "page_count": self.count_pages(reader),
            "metadata": self.extract_metadata(reader),
            "text": self.extract_text(reader), 
            "pages": self.extract_pages(reader),
        }
    
    def extract_metadata(
        self, 
        reader: PdfReader,
    ) -> dict:
        
        metadata = reader.metadata
        
        if metadata is None:
            return {}
        
        return{
            "title": metadata.title,
            "author": metadata.author,
            "subject": metadata.subject,
            "creator": metadata.creator,
            "producer": metadata.producer,
        }
    
    def extract_text(self, reader: PdfReader):
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            
            if page_text:
                text += page_text + "\n"
                
        return text.strip()
    
    def extract_pages(
        self,
        reader: PdfReader,
    ) -> list[dict]:
        """
        Extracts text from each page while preserving page numbers.
        """

        pages: list[dict] = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            page_text = page.extract_text()

            if page_text:
                pages.append(
                    {
                        "page_number": page_number,
                        "text": page_text,
                    }
                )

        return pages
    
    def count_pages(
        self, 
        reader: PdfReader,
    ) -> int:
        
        return len(reader.pages)