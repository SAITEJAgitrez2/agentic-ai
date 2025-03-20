from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_URL = os.getenv("DATABASE_URL") 


def load_pdf_knowledge_base(urls: list[str], collection_name: str = "default_collection"):
    """
    Load and vectorize PDFs using PgVector2 and PDFUrlKnowledgeBase
    :param urls: List of PDF URLs
    :param collection_name: Name of the vector DB collection
    :return: knowledge_base, storage
    """
    # Vector DB setup with PgVector2
    vector_db = PgVector2(
        collection=collection_name,
        db_url=DB_URL,
    )

    # Knowledge base from PDF URLs
    knowledge_base = PDFUrlKnowledgeBase(
        urls=urls,
        vector_db=vector_db
    )

    # Load documents and insert into vector DB
    knowledge_base.load()

    # Assistant chat storage
    storage = PgAssistantStorage(table_name="pdf_assistant", db_url=DB_URL)

    return knowledge_base, storage
