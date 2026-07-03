import logging
from fastapi import FastAPI
from app.core.config import DOCUMENT_STORAGE
from app.api.router import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="AI Research Copilot",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Research Copilot",
        "document_path": str(DOCUMENT_STORAGE)
        }