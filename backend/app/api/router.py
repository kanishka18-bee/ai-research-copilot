from fastapi import APIRouter

from app.api.routes.document import router as document_router
from app.api.routes.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(
    document_router,
    prefix = "/documents",
    tags=["Documents"]
    
)

api_router.include_router(
    chat_router,
)