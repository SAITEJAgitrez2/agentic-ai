import os
from pathlib import Path

project_name = "simple_agentic_ai"

folders = [
    # Backend
    f"{project_name}/backend/app/api",
    f"{project_name}/backend/app/core",
    f"{project_name}/backend/app/knowledge",
    f"{project_name}/backend/app/services",
    f"{project_name}/backend/app/utils",
    f"{project_name}/backend/app/models",
    f"{project_name}/backend/tests",
    
    # Frontend (Next.js + TS + TailwindCSS + Axios + ShadCN + Framer Motion)
    f"{project_name}/frontend/public",
    f"{project_name}/frontend/src/app",
    f"{project_name}/frontend/src/components/ui",
    f"{project_name}/frontend/src/hooks",
    f"{project_name}/frontend/src/lib",
    f"{project_name}/frontend/src/pages",
    f"{project_name}/frontend/src/styles",
    f"{project_name}/frontend/src/utils",
    f"{project_name}/frontend/src/types",
    f"{project_name}/frontend/tests",

    # Config
    f"{project_name}/.github/workflows",
    f"{project_name}/docker",
    f"{project_name}/env"
]

files = [
    # Backend files
    f"{project_name}/backend/app/main.py",
    f"{project_name}/backend/app/api/routes.py",
    f"{project_name}/backend/app/core/config.py",
    f"{project_name}/backend/app/services/assistant_engine.py",
    f"{project_name}/backend/app/utils/db.py",
    f"{project_name}/backend/app/models/schema.py",
    f"{project_name}/backend/requirements.txt",
    f"{project_name}/backend/Dockerfile",

    # Frontend files
    f"{project_name}/frontend/src/app/layout.tsx",
    f"{project_name}/frontend/src/pages/index.tsx",
    f"{project_name}/frontend/src/styles/globals.css",
    f"{project_name}/frontend/src/lib/api.ts",
    f"{project_name}/frontend/package.json",
    f"{project_name}/frontend/tailwind.config.ts",
    f"{project_name}/frontend/postcss.config.js",
    f"{project_name}/frontend/tsconfig.json",
    f"{project_name}/frontend/next.config.js",
    f"{project_name}/frontend/README.md",

    # Shared files
    f"{project_name}/.github/workflows/deploy.yml",
    f"{project_name}/docker/docker-compose.yaml",
    f"{project_name}/Makefile",
    f"{project_name}/env/.env.example",
    f"{project_name}/README.md",
    f"{project_name}/setup.sh"
]

# Create folders and files
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch()

import logging
import pandas as pd
logging.info("✅ Project structure created.")

import shutil
import os

# Display the folder tree structure for verification
def get_directory_structure(rootdir):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        level = dirpath.replace(rootdir, '').count(os.sep)
        indent = '│   ' * level + '├── '
        file_list.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = '│   ' * (level + 1) + '├── '
        for f in filenames:
            file_list.append(f"{subindent}{f}")
    return file_list

structure = get_directory_structure(project_name)

