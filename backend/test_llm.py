from app.services.llm import LLMService

llm = LLMService()

response = llm.generate(
    "Explain Retrieval-Augmented Generation in two sentences."
)

print(response)