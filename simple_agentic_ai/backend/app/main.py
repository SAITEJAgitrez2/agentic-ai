# app/main.py

from fastapi import FastAPI
from app.api.routes import router  # Make sure this path is correct based on your folder structure

app = FastAPI(title="Simple Agentic AI Assistant")

# Register API routes
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Agentic AI Assistant!"}
