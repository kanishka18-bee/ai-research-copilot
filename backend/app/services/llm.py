import logging

from google import genai
from app.core.config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL,
)

logger = logging.getLogger(__name__)


class LLMService:
    """
    Handles communication with the GEMINI language model.
    """
    
    def __init__(self):
        
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )
            
        logger.info(
            "Initializing Gemini client..."
        )   
        
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )
        
        self.model_name = GEMINI_MODEL
        
        logger.info(
            "Gemini client initialized successfully (model=%s).",
            self.model_name,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        
        if not prompt or not prompt.strip():
            logger.warning("Prompt is empty.")
            
            raise ValueError(
                "Prompt cannot be empty."
            )
             
        logger.info(
            "Generating response from Gemini..."
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        
        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )
            
        logger.info(
            "Response generated successfully."      
        )
        
        return response.text
    
        logger.exception(
            "Failed to generate response from Gemini."
        )
        raise