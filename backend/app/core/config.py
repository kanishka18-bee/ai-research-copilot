from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENT_STORAGE = PROJECT_ROOT / os.getenv(
    "DOCUMENT_STORAGE",
    "storage/documents"
)

EMBEDDING_STORAGE = PROJECT_ROOT / os.getenv(
    "EMBEDDING_STORAGE",
    "storage/embeddings"
)

EXPORT_STORAGE = PROJECT_ROOT / os.getenv(
    "EXPORT_STORAGE",
    "storage/exports"
)

TEMP_STORAGE = PROJECT_ROOT / os.getenv(
    "TEMP_STORAGE",
    "storage/temp"
)

MAX_FILE_SIZE = int(
    os.getenv("MAX_FILE_SIZE", 52428800)
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
