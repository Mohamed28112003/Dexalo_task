from typing import List, Optional, Dict, Any
from ChromaDBManager import ChromaDBManager
from AnswerGenerator import AnswerGenerator
from LLMProvider import LLMProvider
from PromptManager import PromptManager
from langchain.schema import Document


class RAGPipelineManager:
    """
    Manager class that orchestrates the RAG (Retrieval Augmented Generation) pipeline,
    connecting vector database retrieval with LLM-based answer generation.
    """
    
    def __init__(
        self,
        db_manager: ChromaDBManager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        retrieval_k: int = 4
    ):
        """
        Initialize the RAG pipeline manager.
        
        Args:
            db_manager: ChromaDBManager instance for document retrieval
            llm_provider: LLMProvider instance for language model access
            prompt_manager: PromptManager instance for prompt templates
            retrieval_k: Number of documents to retrieve
        """
        self.db_manager = db_manager
        self.answer_generator = AnswerGenerator(llm_provider, prompt_manager)
        self.retrieval_k = retrieval_k
    
    def retrieve_documents(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents based on the query using similarity search.
        
        Args:
            query: User query string
            
        Returns:
            List of relevant Document objects
        """
        return self.db_manager.similarity_search(
            query=query,
            k=self.retrieval_k
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query through the full RAG pipeline.
        
        Args:
            query: User query string
            
        Returns:
            Dictionary containing the answer and metadata about the process
        """
        # Start with document retrieval
        retrieved_docs = self.retrieve_documents(query)
        
        # Track document sources for citation
        sources = []
        for doc in retrieved_docs:
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                if doc.metadata['source'] not in sources:
                    sources.append(doc.metadata['source'])
        
        # Generate answer from retrieved documents
        answer = self.answer_generator.generate_answer(query, retrieved_docs)
        
        # Return answer and metadata
        return {
            "query": query,
            "answer": answer,
            "num_docs_retrieved": len(retrieved_docs),
            "sources": sources,
            "documents": retrieved_docs
        }
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get basic statistics about the vector store collection"""
        return {
            "document_count": self.db_manager.get_collection_count()
        }