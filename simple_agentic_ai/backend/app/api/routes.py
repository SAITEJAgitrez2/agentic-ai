from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.core.services.assistant_engine import agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "user"  # Optional: use UUID for multi-user later

@router.post("/chat")
async def chat(request: ChatRequest):
    response = agent.chat(request.message)
    return {"response": response}
