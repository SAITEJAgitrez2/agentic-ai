from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.core.services.assistant_engine import agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "user"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = agent.respond(request.message, stream=False)  # use respond
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
