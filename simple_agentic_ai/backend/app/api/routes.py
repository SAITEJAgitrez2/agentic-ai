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

        # Call `.load()` with the new URLs
        agent.knowledge.urls = pdf_urls  # update the urls dynamically
        agent.knowledge.load(recreate=False, upsert=True)

        print("✅ PDF ingestion complete")
        return {"message": f"{len(pdf_urls)} PDFs ingested successfully."}
    except Exception as e:
        print("❌ Error during ingestion:", str(e))
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/ingest/upload")
async def ingest_pdf_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        agent.knowledge.load_file(file=contents, filename=file.filename, upsert=True)
        return {"message": "PDF uploaded and ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))