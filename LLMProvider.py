from typing import List, Optional
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMProvider:
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        openai_api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 300
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")

        self.model = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.llm = self.initialize_llm()

    def initialize_llm(self):
        return ChatOpenAI(
            api_key=self.openai_api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    def get_llm(self):
        return self.llm