from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingProvider(OpenAIEmbeddings):

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        openai_api_key: Optional[str] = None
    ):
        supported_models = ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]
        if model_name not in supported_models:
            raise ValueError(f"Unsupported model: {model_name}. Choose from {supported_models}")
        
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        super().__init__(model=model_name, openai_api_key=openai_api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
     
        return super().embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
       
        return super().embed_query(query)