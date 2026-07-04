from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """ 
    Request body for chat query
    """
    
    question: str = Field(
        ...,
        min_length=1,
        description="The users's question about the uploaded documents.",
    )
    
class ChatResponse(BaseModel):
        """ 
        Response returned by the chat endpoint
        """
        
        answer: str 