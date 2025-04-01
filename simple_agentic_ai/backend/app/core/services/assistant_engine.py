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

logging.basicConfig(
    filename="./app.log",  # <- make sure this path is valid
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 1. Database connection URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 2. Shared vector store for both file and URL knowledge
vector_db = PgVector(table_name="pdf_documents", db_url=db_url)

# 3. File-based knowledge base (used at startup)
file_knowledge_base = PDFKnowledgeBase(
    path="/home/saiteja/agentic-ai/simple_agentic_ai/backend/data/pdfs/NIPS-2012-imagenet-classification-with-deep-convolutional-neural-networks-Paper.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True)
)

# Optional: Load existing files on startup
file_knowledge_base.load(recreate=True, upsert=True)

# 4. URL-based knowledge base (used dynamically per request)
def get_url_kb(urls: list):
    return PDFUrlKnowledgeBase(
        urls=urls,
        vector_db=vector_db
    )

# Agent setup
agent = Agent(
    session_id="user",         # default session_id
    user_id="user",            # required for storage
    model=OpenAIChat(id="gpt-4o"),
    knowledge=file_knowledge_base,
    memory=AgentMemory(
        db=PgMemoryDb(table_name="agent_memory", db_url=db_url),
        create_user_memories=True,
        create_session_summary=True,
    ),
    storage=vector_db,
    add_history_to_messages=True,
    num_history_responses=3,
    read_chat_history=True,
)