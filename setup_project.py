import os
from pathlib import Path


def build_project_structure(base_dir):
    # Define our modular folders
    folders = [
        "src",
        "data"
    ]

    # 1. Create folders programmatically
    for folder in folders:
        Path(os.path.join(base_dir, folder)).mkdir(
            parents=True,
            exist_ok=True
        )

    # 2. Define our default boilerplate file contents
    files = {
        ".env": (
            "YOUTUBE_API_KEY=your_key_here\n"
            "TELEGRAM_BOT_TOKEN=your_token_here\n"
            "TELEGRAM_CHAT_ID=your_id_here"
        ),

        ".gitignore": (
            ".env\n"
            "__pycache__/\n"
            "data/*.csv\n"
            ".ipynb_checkpoints/"
        ),

        "requirements.txt": (
            "pandas\n"
            "numpy\n"
            "scikit-learn\n"
            "streamlit\n"
            "requests\n"
            "python-dotenv"
        ),

        "src/__init__.py": "",
        "src/data_ingestion.py": "# YouTube data fetching logic\n",
        "src/ml_pipeline.py": "# Scikit-learn Random Forest classification\n",
        "src/alert_system.py": "# Telegram Bot alert mechanisms\n",
        "src/app.py": "# Streamlit dashboard interface\n"
    }

    # 3. Generate files programmatically
    for file_path, default_content in files.items():
        full_path = os.path.join(base_dir, file_path)

        if not os.path.exists(full_path):
            with open(full_path, "w") as f:
                f.write(default_content)

            print(f"Successfully created: {file_path}")
        else:
            print(f"Skipped: {file_path} (Already exists)")


if __name__ == "__main__":

    # Use the folder where this Python script is located
    project_root = Path(__file__).resolve().parent

    print(f"Starting automation script inside {project_root}...\n")

    build_project_structure(project_root)

    print("\nInitialization complete! Your workspace is fully set up.")