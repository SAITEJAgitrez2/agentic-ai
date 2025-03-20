import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "agentic_ai"

list_of_files = [
    ".github/workflows/.gitkeep",

    # Backend Structure
    f"{project_name}_backend/app/__init__.py",
    f"{project_name}_backend/app/api/__init__.py",
    f"{project_name}_backend/app/api/routes.py",
    f"{project_name}_backend/app/core/__init__.py",
    f"{project_name}_backend/app/core/config.py",
    f"{project_name}_backend/app/services/__init__.py",
    f"{project_name}_backend/app/services/assistant_engine.py",
    f"{project_name}_backend/app/utils/__init__.py",
    f"{project_name}_backend/app/utils/db.py",
    f"{project_name}_backend/app/main.py",
    f"{project_name}_backend/app/knowledge/pdf_loader.py",

    f"{project_name}_backend/requirements.txt",
    f"{project_name}_backend/Dockerfile",

    # Frontend Structure (React)
    f"{project_name}_frontend/src/components/.gitkeep",
    f"{project_name}_frontend/src/pages/.gitkeep",
    f"{project_name}_frontend/src/App.js",
    f"{project_name}_frontend/src/index.js",
    f"{project_name}_frontend/package.json",
    f"{project_name}_frontend/tailwind.config.js",
    f"{project_name}_frontend/postcss.config.js",
    f"{project_name}_frontend/Dockerfile",

    # Shared files
    "docker-compose.yaml",
    "README.md",
    "setup.sh",
    "Makefile",
    "env/.env",
    "tests/test_backend.py",
    "tests/test_frontend.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info("✅ Project scaffolding complete.")
