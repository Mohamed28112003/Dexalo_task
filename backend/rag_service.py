# File: backend/rag_service.py
from TextProcessor import TextProcessor
from ChromaDBManager import ChromaDBManager
from LLMProvider import LLMProvider
from PromptManager import PromptManager
from RAGPipelineManager import RAGPipelineManager

from dotenv import load_dotenv
import os
load_dotenv()
def get_rag_pipeline():
    docs_directory = os.getenv("docs_directory")
    print(f"Docs directory: {docs_directory}")
    db_directory = os.getenv("db_directory")
    print(f"DB directory: {db_directory}")

    processor = TextProcessor(directory_path=docs_directory)
    processed_docs = processor.process_documents(chunk_size=600, chunk_overlap=200)

    chroma_db = ChromaDBManager(path=db_directory)
    chroma_db.add_documents(processed_docs)

    llm_provider = LLMProvider()
    prompt_manager = PromptManager()

    rag_pipeline = RAGPipelineManager(
        db_manager=chroma_db,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        retrieval_k=4
    )
    return rag_pipeline



