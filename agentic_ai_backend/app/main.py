from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Agentic AI Backend")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": " Agentic AI Assistant API is up and running!"}