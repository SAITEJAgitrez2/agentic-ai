from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from phi.assistant.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
db_url = os.getenv("DATABASE_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")

# Initialize FastAPI
app = FastAPI(title="Simple Agentic AI Assistant")

# Knowledge base and storage
storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

class ChatRequest(BaseModel):
    message: str
    user: str = "user"

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat messages from the frontend."""
    try:
        assistant = Assistant(
            run_id=None,
            user_id=request.user,
            knowledge_base=None,
            storage=storage,
            show_tool_calls=True,
            search_knowledge=True,
            read_chat_history=True,
        )
        response = assistant.chat(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/url")
async def ingest_pdf_url(pdf_urls: List[str]):
    """Ingest PDFs via URL."""
    try:
        vector_db = PgVector2(collection="pdf_collection", db_url=db_url)
        knowledge_base = PDFUrlKnowledgeBase(urls=pdf_urls, vector_db=vector_db)
        knowledge_base.load()
        return {"message": "PDFs successfully ingested"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/upload")
async def ingest_pdf_upload(file: UploadFile = File(...)):
    """Ingest PDFs via file upload."""
    try:
        file_path = f"temp_uploads/{file.filename}"
        os.makedirs("temp_uploads", exist_ok=True)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Process the uploaded PDF (dummy example)
        vector_db = PgVector2(collection="pdf_collection", db_url=db_url)
        knowledge_base = PDFUrlKnowledgeBase(urls=[file_path], vector_db=vector_db)
        knowledge_base.load()
        
        return {"message": f"File '{file.filename}' successfully ingested"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
