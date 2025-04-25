from typing import List, Any
from LLMProvider import LLMProvider

from langchain.schema import Document
from PromptManager import PromptManager

class AnswerGenerator:
    """Class for generating answers from retrieved documents"""

    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.generation_prompt = self.prompt_manager.get_prompt("generation_prompt")
    
    def format_context(self, documents: List[Document]) -> str:
        """Format the documents into a context string"""
        return "\n\n".join([doc.page_content for doc in documents])
    
    def handle_response(self, response: Any) -> str:
        """Extract content from different response types"""
        if hasattr(response, 'content'):
            return response.content
        return str(response)

    def generate_answer(self, query: str, documents: List[Document]) -> str:
        """Generate an answer based on query and retrieved documents"""
        try:
            context = self.format_context(documents)
            
            prompt = self.generation_prompt.format(
                context=context,
                question=query
            )

            llm = self.llm_provider.get_llm()
            response = llm.invoke(prompt)

            return self.handle_response(response)

        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"Failed to generate an answer: {str(e)}"