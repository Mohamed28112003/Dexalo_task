from langchain_chroma import Chroma
from langchain.schema import Document
from typing import List
from EmbeddingProvider import EmbeddingProvider 

from typing import Optional


class ChromaDBManager:
    def __init__(
        self,
        path: str,
        collection_name: str = 'Book',
        openai_api_key: Optional[str] = None,
        model_name: str = "text-embedding-3-small"
    ):
        self.embedding_function = EmbeddingProvider(
            model_name=model_name,
            openai_api_key=openai_api_key
        )
        self.vector_store = Chroma(
            collection_name=collection_name,
            persist_directory=path,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Document]):
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=ids)
        # manual persist no longer needed
        print(f"Stored {len(documents)} documents.")

    def similarity_search(self, query: str, k: int = 2) -> List[Document]:
        return self.vector_store.similarity_search(query, k)

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 2,
        fetch_k: int = 12
    ) -> List[Document]:
        return self.vector_store.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)

    def get_collection_count(self) -> int:
        return self.vector_store._collection.count()