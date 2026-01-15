from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import tempfile
from pathlib import Path

# Import existing logic
# Note: We need to ensure src is in python path or relative imports work
# Since this file is in src/api/, we might need to adjust imports or run from root
import sys
# Add src to path to allow imports from sibling directories
sys.path.append(str(Path(__file__).parent.parent))

from retrieval import retrieve_similar_docs
from llm import final_answer
from data_loader import document_handler

app = FastAPI(title="RAG Chatbot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str

class FileUploadResponse(BaseModel):
    filename: str
    status: str
    chunks_processed: int = 0

# Adapter class to mimic Streamlit's UploadedFile or standard file object
class FileAdapter:
    def __init__(self, file: UploadFile, temp_path: str):
        self.file = file
        self.name = file.filename
        self.temp_path = temp_path

    def read(self):
        with open(self.temp_path, "rb") as f:
            return f.read()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Retrieve context
        similar_docs = retrieve_similar_docs(request.message)
        
        if not similar_docs:
            return ChatResponse(response="I couldn't find any relevant information in the uploaded documents.")
            
        # Generate answer
        answer = final_answer(similar_docs, request.message)
        return ChatResponse(response=answer)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file to temp file to be read by data_loader
        # data_loader expects a file-like object with .name and .read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            # Create adapter
            adapter = FileAdapter(file, tmp_path)
            
            # Process document
            # Note: document_handler returns a list of LangChain Documents
            # We probably need to store them in the vector store here? 
            # Checking retrieval.py, it uses 'vectordb' global object.
            # data_loader just returns docs. We need to ingest them.
            
            docs = document_handler(adapter)
            
            if not docs:
                raise HTTPException(status_code=400, detail="Could not process file")

            # We need to add these docs to the vector store
            # Import vectordb from retrieval to add documents
            from retrieval import vectordb
            
            # Persist documents
            vectordb.add_documents(docs)
            
            return FileUploadResponse(
                filename=file.filename,
                status="success",
                chunks_processed=len(docs)
            )
            
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
