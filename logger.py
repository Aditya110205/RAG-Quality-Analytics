import json
from pathlib import Path


LOG_FILE = Path("logs/queries.jsonl")


def log_query(event: dict):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")