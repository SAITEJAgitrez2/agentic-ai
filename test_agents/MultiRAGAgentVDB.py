from agno.agent import Agent, AgentMemory
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.memory.db.postgres import PgMemoryDb

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# PostgreSQL connection URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Set up the vector store with correct table name
vector_db = PgVector(table_name="latest_ai_paper", db_url=db_url)

# Set up PDF knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://fcs.tennessee.edu/wp-content/uploads/sites/23/2021/08/Cooking-Basics.pdf"],
    vector_db=vector_db
)

# Load the PDF embeddings
knowledge_base.load(recreate=True, upsert=True)

# Agent setup with memory and knowledge
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    memory=AgentMemory(
        db=PgMemoryDb(table_name="agent_memory", db_url=db_url),
        create_user_memories=True,
        create_session_summary=True,
    ),
    storage=PostgresAgentStorage(table_name="pdf_assistant_sessions", db_url=db_url),
    add_history_to_messages=True,
    num_history_responses=3,
    read_chat_history=True,
)

if __name__ == "__main__":
    print("Starting Agentic Assistant...\n")
    while True:
        try:
            query = input("You: ")
            if query.lower() in {"exit", "quit"}:
                print("Exiting Assistant. Goodbye!")
                break
            agent.print_response(query, stream=True)
        except KeyboardInterrupt:
            print("\nExiting Assistant. Goodbye!")
            break
