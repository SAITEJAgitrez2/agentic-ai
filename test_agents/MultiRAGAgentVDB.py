import typer
from typing import Optional, List
from phi.assistant import assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.vectordb.pgvector.pgvector2 import PgVector2

from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Define PostgreSQL DB URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Step 1: Download PDF from URL and save it locally
pdf_url = "https://arxiv.org/pdf/2503.12937"
pdf_path = "latest_ai_paper.pdf"

if not os.path.exists(pdf_path):
    print(f"📥 Downloading PDF from {pdf_url}...")
    response = requests.get(pdf_url)
    with open(pdf_path, "wb") as f:
        f.write(response.content)
    print("✅ PDF downloaded and saved locally.")

# Step 2: Define a local embedding wrapper
class LocalEmbeddingWrapper:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embedding_and_usage(self, text):
        embedding = self.model.encode(text, normalize_embeddings=True).tolist()
        return embedding, None
    @property
    def dimensions(self):
        return self.model.get_sentence_embedding_dimension()


# Step 3: Initialize vector DB and drop existing collection if dimension mismatch
vector_db = PgVector2(
    collection="latest_ai_paper",
    db_url=db_url,
    embedder=LocalEmbeddingWrapper()
)

# Reset the collection to fix dimension mismatch
vector_db.drop_collection()  # <-- Add this line

# Step 4: Initialize PDFKnowledgeBase
knowledge_base = PDFKnowledgeBase(
    path=pdf_path,
    vector_db=vector_db
)

# Step 5: Load knowledge base
print("📚 Loading knowledge base...")
knowledge_base.load()


# Step 6: Set up assistant storage in Postgres
storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

# Step 7: Define the assistant logic
def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    chat_assistant = assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )

    if run_id is None:
        run_id = chat_assistant.run_id
        print(f"🆕 New Assistant Run Started: {run_id}\n")
    else:
        print(f"🔄 Continuing Assistant Run: {run_id}\n")

# Step 8: Run it via CLI
if __name__ == "__main__":
    typer.run(pdf_assistant)
