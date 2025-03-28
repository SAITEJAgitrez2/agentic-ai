from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.services.assistant_engine import agent

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
