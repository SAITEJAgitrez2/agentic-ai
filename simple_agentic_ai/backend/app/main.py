# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router  # Make sure this path is correct

app = FastAPI(title="Simple Agentic AI Assistant")

# Enable CORS (allow frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # safer than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Agentic AI Assistant!"}
