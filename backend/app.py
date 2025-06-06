# app.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
from typing import List
import uuid
import uvicorn
from pydantic import BaseModel
from pathlib import Path
import time
from dotenv import load_dotenv

from TextProcessor import TextProcessor
from ChromaDBManager import ChromaDBManager
from LLMProvider import LLMProvider
from PromptManager import PromptManager
from RAGPipelineManager import RAGPipelineManager

from agent import MathAgent

load_dotenv()

app = FastAPI(title="RAG and Math API", description="API for document RAG pipeline and mathematical calculations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[str] = []
    processing_time: float

class MathRequest(BaseModel):
    expression: str

class MathResponse(BaseModel):
    expression: str
    result: str
    processing_time: float

DOCS_DIRECTORY = os.getenv("docs_directory")
DB_DIRECTORY = os.getenv("db_directory")
ALLOWED_EXTENSIONS = {"txt", "pdf"}

Path(DOCS_DIRECTORY).mkdir(parents=True, exist_ok=True)
Path(DB_DIRECTORY).mkdir(parents=True, exist_ok=True)

rag_pipeline = None

math_agent = MathAgent()

def file_extension_is_valid(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def build_rag_pipeline():
    """Build/rebuild the RAG pipeline with current documents"""
    processor = TextProcessor(directory_path=DOCS_DIRECTORY)
    processed_docs = processor.process_documents(chunk_size=600, chunk_overlap=200)
    
    chroma_db = ChromaDBManager(path=DB_DIRECTORY)
    chroma_db.add_documents(processed_docs)
    
    llm_provider = LLMProvider()
    prompt_manager = PromptManager()
    
    return RAGPipelineManager(
        db_manager=chroma_db,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        retrieval_k=4
    )

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup if documents exist"""
    global rag_pipeline
    if any(Path(DOCS_DIRECTORY).iterdir()):
        rag_pipeline = build_rag_pipeline()

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple files and rebuild the RAG pipeline"""
    global rag_pipeline
    
    uploaded_files = []
    for file in files:
        if not file_extension_is_valid(file.filename):
            raise HTTPException(status_code=400, detail=f"File {file.filename} has an invalid extension. Allowed: {ALLOWED_EXTENSIONS}")

        file_path = os.path.join(DOCS_DIRECTORY, file.filename)
       
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append(file.filename)
    
    
    rag_pipeline = build_rag_pipeline()
    
    return JSONResponse(
        status_code=200,
        content={"message": f"Successfully uploaded {len(uploaded_files)} files", "files": uploaded_files}
    )

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG pipeline with a question"""
    global rag_pipeline
    
    if not rag_pipeline:
        raise HTTPException(status_code=404, detail="No documents have been uploaded yet. Please upload documents first.")
    
    start_time = time.time()
    result = rag_pipeline.process_query(request.query)
    processing_time = time.time() - start_time
    
    
    sources = []
    if "sources" in result:
        sources = result["sources"]
    
    return QueryResponse(
        query=result["query"],
        answer=result["answer"],
        sources=sources,
        processing_time=round(processing_time, 2)
    )

@app.post("/math", response_model=MathResponse)
async def calculate_math(request: MathRequest):
    """Process mathematical calculations using MathAgent"""
    global math_agent
    
    start_time = time.time()
    try:
        result = math_agent.run(request.expression)
        processing_time = time.time() - start_time
        
        return MathResponse(
            expression=request.expression,
            result=result,
            processing_time=round(processing_time, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing mathematical expression: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    files = [f.name for f in Path(DOCS_DIRECTORY).iterdir() if f.is_file()]
    return {"documents": files, "count": len(files)}

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a specific document"""
    file_path = Path(DOCS_DIRECTORY) / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Document {filename} not found")
    
    file_path.unlink()
    
   
    global rag_pipeline
    if any(Path(DOCS_DIRECTORY).iterdir()):
        rag_pipeline = build_rag_pipeline()
    else:
        rag_pipeline = None
    
    return {"message": f"Document {filename} deleted successfully"}

@app.delete("/documents")
async def delete_all_documents():
    """Delete all documents"""
    for file_path in Path(DOCS_DIRECTORY).iterdir():
        if file_path.is_file():
            file_path.unlink()
    
    
    global rag_pipeline
    rag_pipeline = None
    
    return {"message": "All documents deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)