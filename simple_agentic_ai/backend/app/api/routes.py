from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.services.assistant_engine import agent
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "user"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        agent.session_id = request.session_id
        result = agent.run(request.message)
        return {"response": result.content} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/ingest/url")
async def ingest_pdf_url(payload: dict):
    try:
        pdf_urls = payload.get("pdf_urls", [])
        print("🧾 Ingesting URLs:", pdf_urls)
        if not pdf_urls:
            raise ValueError("No PDF URLs provided.")

        # Use PDFUrlKnowledgeBase here
        from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
        from app.core.services.assistant_engine import vector_db

        kb = PDFUrlKnowledgeBase(urls=pdf_urls, vector_db=vector_db)
        kb.load(upsert=True)

        # Update agent knowledge if you want to query it immediately
        from app.core.services.assistant_engine import agent
        agent.knowledge = kb

        return {"message": f"{len(pdf_urls)} PDFs ingested successfully."}
    except Exception as e:
        print("❌ Error during ingestion:", str(e))
        raise HTTPException(status_code=400, detail=f"❌ Error during ingestion: {str(e)}")



import os

from app.core.services.assistant_engine import agent, vector_db
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader

@router.post("/ingest/upload")
async def ingest_pdf_upload(file: UploadFile = File(...)):
    try:
        upload_dir = "data/pdfs"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Recreate knowledge base with updated path
        updated_kb = PDFKnowledgeBase(
            path=upload_dir,
            vector_db=vector_db,
            reader=PDFReader(chunk=True),
        )
        updated_kb.load(upsert=True)
        agent.knowledge = updated_kb  # <-- Update the agent's knowledge

        return {"message": "✅ PDF uploaded and ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Upload failed: {str(e)}")

from fastapi.responses import JSONResponse

@router.get("/history")
async def get_history(session_id: str = "user"):
    try:
        agent.session_id = session_id  # make sure agent is in correct session
        messages = agent.memory.get_messages()
        return {"messages": [m.model_dump(include={"role", "content"}) for m in messages]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/logs")
async def get_logs():
    try:
        with open("app/app.log", "r") as f:
            log_data = f.read().splitlines()[-100:]  # latest 100 lines
        return {"logs": log_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))