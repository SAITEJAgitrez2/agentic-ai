# Agentic AI Assistant

A fully functional, modular Agentic AI system built using FastAPI, React, LangChain, OpenAI, PgVector, and Docker. This application enables autonomous task execution, RAG-based knowledge search, and PDF knowledge ingestion via intelligent agents.


🚀 Features:
----------------------------------------------------
- FastAPI-powered REST API backend
- PDFUrlKnowledgeBase with vector search
- PgVector (Postgres) vector database
- OpenAI LLM assistant with RAG architecture
- React-based interactive frontend
- Docker-based deployment
- Scalable modular structure

⚙️ Setup Instructions:
----------------------------------------------------
1. Clone the repository
   git clone https://github.com/yourusername/agentic-ai-assistant.git
   cd agentic-ai-assistant

2. Set up environment
   cp env/.env.example env/.env
   # Edit .env to include your keys and DB credentials

3. Run with Docker Compose
   docker-compose up --build

   → Frontend: http://localhost:3000
   → Backend API: http://localhost:8000/docs

🔐 Environment Variables:
----------------------------------------------------
OPENAI_API_KEY=your_openai_api_key
DB_URL=postgresql+psycopg://username:password@host:port/dbname

🧠 Core Capabilities:
----------------------------------------------------
- Autonomous Agent Orchestration (via LangChain)
- PDF Document Chunking and Embedding
- RAG Search over Vector Database
- Memory-aware Assistant Conversations
- CLI & Web-based Assistant Interface

📚 Use Cases:
----------------------------------------------------
- AI-powered research assistant
- Customer support document search
- Autonomous task execution engine
- Document intelligence applications


🧪 Testing:
----------------------------------------------------
Run tests using:
   pytest tests/

🙌 Acknowledgments:
----------------------------------------------------
- LangChain
- HuggingFace
- OpenAI
- PgVector
- Inspired by Krish Naik’s Agentic AI System

📬 Contact:
----------------------------------------------------
Sai Teja  
Email: saiteja.cse.rymec@gmail.com  
LinkedIn: https://linkedin.com/in/saitejanv

====================================================
⭐ Star This Project:
----------------------------------------------------
If you find this project useful, please give it a ⭐ on GitHub!
