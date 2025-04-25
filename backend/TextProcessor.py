from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from typing import List, Optional
from langchain.schema import Document
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class TextProcessor:

    def __init__(self, directory_path: str, file_types: Optional[List[str]] = None):

        self.directory_path = directory_path
        self.file_types = file_types or ["*.txt", "*.pdf"]
        
        # Validate directory exists
        if not os.path.isdir(directory_path):
            raise ValueError(f"Directory not found: {directory_path}")

    def load_documents(self) -> List[Document]:
        loader = DirectoryLoader(
            self.directory_path,
            glob=self.file_types,
            show_progress=False
        )
        return loader.load()

    @staticmethod
    def split_text_recursive(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(documents)

    @staticmethod
    def clean_text(text: str) -> str:

        if not isinstance(text, str) or not text.strip():
            return ""
        
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove special characters except punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def process_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:

    
        documents = self.load_documents()
        
        if not documents:
            return []
            
        with ThreadPoolExecutor() as executor:
            futures = []
            for doc in documents:
                futures.append(
                    executor.submit(self._clean_document, doc)
                )
            
            cleaned_docs = []
            for future in as_completed(futures):
                cleaned_docs.append(future.result())
        
        doc_splits = self.split_text_recursive(cleaned_docs, chunk_size, chunk_overlap)
        
        for i, doc in enumerate(doc_splits):
            if doc.metadata is None:
                doc.metadata = {}
            doc.metadata['chunk_id'] = i + 1
            
        return doc_splits
    
    @staticmethod
    def _clean_document(doc: Document) -> Document:
        """Helper method to clean a single document for parallel processing."""
        doc.page_content = TextProcessor.clean_text(doc.page_content)
        return doc