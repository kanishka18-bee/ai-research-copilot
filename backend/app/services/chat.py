import logging

from app.services.search import SearchService
from app.services.prompt_builder import PromptBuilder
from app.services.llm import LLMService

logger = logging.getLogger(__name__)


class ChatService:
    """
    Coordinates the complete Retrieval-Augmented Generation (RAG) pipeline by retrieving relevant context, building a prompt, and generating a response from the language model.
    """


    def __init__(
        self,
        search_service: SearchService,
        prompt_builder: PromptBuilder,
        llm_service: LLMService,
    ):
        self.search_service = search_service
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    def chat(
        self,
        question: str,
    ) -> str:
        
        if not question or not question.strip():
            logger.warning("Question is empty.")
            raise ValueError(
                "Question cannot be empty."
            )
        
        logger.info(
            "Processing chat request through RAG pipeline."
        )
        
        try: 
            
            results = self.search_service.search(question)

            if not results:
                logger.info(
                    "No relevant context found."
                )
                return (
                    "I couldn't find any relevant information related to your question in the uploaded documents."
            )
            
            prompt = self.prompt_builder.build_prompt(
                question,
                results
            )
        
            answer = self.llm_service.generate(prompt)
        
            logger.info(
                "Chat response generated successfully."
            )
        
            return answer
        
        except Exception:
            logger.exception(
                "Chat request failed."
            )
            raise