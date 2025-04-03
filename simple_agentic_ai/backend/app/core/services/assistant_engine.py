from agno.agent import Agent, AgentMemory
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pgvector import PgVector
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.memory.db.postgres import PgMemoryDb
import os
from dotenv import load_dotenv
import logging

# Logging setup
logging.basicConfig(
    filename="./app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#PostgreSQL connection URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

#Shared vector store (for both file & URL ingestion)
vector_db = PgVector(table_name="pdf_documents", db_url=db_url)

# File-based knowledge base (used at startup)
file_knowledge_base = PDFKnowledgeBase(
    path="/home/saiteja/agentic-ai/simple_agentic_ai/backend/data/pdfs/NIPS-2012-imagenet-classification-with-deep-convolutional-neural-networks-Paper.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

# 4. Load PDF documents into the vector DB
file_knowledge_base.load(recreate=True, upsert=True)

#URL-based knowledge base (used for dynamic ingestion)
def get_url_kb(urls: list):
    return PDFUrlKnowledgeBase(
        urls=urls,
        vector_db=vector_db,
    )

# Agent Setup with Correct Persistent Memory and Storage
agent = Agent(
    session_id="user",      # Default session ID
    user_id="user",         # Required for memory and storage
    model=OpenAIChat(id="gpt-4o"),
    knowledge=file_knowledge_base,
    memory=AgentMemory(
        db=PgMemoryDb(table_name="agent_memory", db_url=db_url),
        create_user_memories=True,
        create_session_summary=True
    ),
    storage=PostgresAgentStorage(table_name="assistant_sessions", db_url=db_url),
    add_history_to_messages=True,
    num_history_responses=3,
    read_chat_history=True,
)
