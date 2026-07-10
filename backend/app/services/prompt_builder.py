import logging
from textwrap import dedent

from app.services.vector_store import SearchResult


logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Builds prompts for the language model using the user's
    question and retrieved document context.
    """

    def build_prompt(
        self,
        question: str,
        context: list[SearchResult],
    ) -> str:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not context:
            raise ValueError("Context cannot be empty.")

        context_blocks: list[str] = []

        for i, result in enumerate(context):
            page = (
                f"Page: {result.metadata.page_number}"
                if result.metadata.page_number is not None
                else "Page: Unknown"
            )

            context_blocks.append(
                dedent(
                    f"""
                    Context {i + 1}

                    Document: {result.metadata.filename}
                    {page}

                    Content:
                    {result.metadata.chunk}
                    """
                ).strip()
            )

        context_text = "\n\n".join(context_blocks)

        prompt = dedent(
            f"""
        You are an AI research assistant.

        Answer the user's question using ONLY the provided context.

        If the answer is not present in the context, reply exactly:

        "I couldn't find that information in the uploaded documents."

        Do not use outside knowledge.
        Do not make up facts.
        Keep the answer concise, accurate, and based only on the retrieved context.
        
        Every factual statement in your answer must include its supporting document name and page number in parentheses.

        Example:
        The model uses Graph Neural Networks (Source: paper.pdf, Page 7).
        
        ------------------------
        Context
        ------------------------

        {context_text}

        ------------------------
        Question
        ------------------------

        {question}

        ------------------------
        Answer
        ------------------------
        """
        )

        logger.info(
            "Prompt built successfully using %d context chunks.",
            len(context),
        )

        return prompt.strip()
