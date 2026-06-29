from pathlib import Path
from pypdf import PdfReader

class PDFParser:
    
    def parse(self, file_path: Path) -> dict:
        reader = PdfReader(file_path)
        
        return{
            "page_count": self.count_pages(reader),
            "metadata": self.extract_metadata(reader),
            "text": self.extract_text(reader), 
        }
    
    def extract_metadata(self, reader: PdfReader):
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
    
    def count_pages(self, reader: PdfReader):
        return len(reader.pages)