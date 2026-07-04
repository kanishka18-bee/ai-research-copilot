from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest, 
    ChatResponse,
)

from app.dependencies.services import (
    chat_service,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)

def chat(
    request: ChatRequest
) -> ChatResponse:
    """
    Handle a chat request and return the response.
    """
    answer = chat_service.chat(
        request.question,
    )
    
    return ChatResponse(
        answer=answer,
    )
    