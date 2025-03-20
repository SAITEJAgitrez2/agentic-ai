from agentic_ai_backend.app.knowledge.pdf_loader import PDFKnowledgeLoader
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.assistant.assistant import Assistant
import os
from dotenv import load_dotenv

load_dotenv()

class AssistantEngine:
    def __init__(self, db_url: str, pdf_urls: list[str], table_name: str = "pdf_assistant", user: str = "user"):
        self.db_url = db_url
        self.pdf_urls = pdf_urls
        self.table_name = table_name
        self.user = user

        # Initialize PDF knowledge base loader
        self.knowledge_loader = PDFKnowledgeLoader(db_url=self.db_url, urls=self.pdf_urls)

        # Initialize storage for assistant memory/context
        self.storage = PgAssistantStorage(table_name=self.table_name, db_url=self.db_url)

    def load_knowledge_base(self):
        """Load and vectorize documents into PgVector2"""
        self.knowledge_base = self.knowledge_loader.load_and_vectorize()

    def launch_assistant(self, new: bool = False):
        from typing import Optional

        run_id: Optional[str] = None
        if not new:
            existing_run_ids = self.storage.get_all_run_ids(self.user)
            if existing_run_ids:
                run_id = existing_run_ids[0]

        assistant = Assistant(
            run_id=run_id,
            user_id=self.user,
            knowledge_base=self.knowledge_base,
            storage=self.storage,
            show_tool_calls=True,
            search_knowledge=True,
            read_chat_history=True,
        )

        if run_id is None:
            run_id = assistant.run_id
            print(f"✅ Started New Run: {run_id}\n")
        else:
            print(f"➡️ Continuing Run: {run_id}\n")

        assistant.cli_app(markdown=True)


if __name__ == "__main__":
    # Example execution
    PDF_URLS = [
        "https://fcs.tennessee.edu/wp-content/uploads/sites/23/2021/08/Cooking-Basics.pdf"
    ]
    DB_URL = os.getenv("PGVECTOR_DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")

    engine = AssistantEngine(db_url=DB_URL, pdf_urls=PDF_URLS)
    engine.load_knowledge_base()
    engine.launch_assistant(new=False)
