from pathlib import Path


DATA_DIR = Path("data")

CHUNK_SIZE = 256
OVERLAP = 25


def chunk_text(text: str) -> list[str]:
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = end - OVERLAP

    return chunks


def load_documents() -> list[dict]:
    documents = []

    for path in DATA_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            documents.append(
                {
                    "id": f"{path.stem}_{index}",
                    "text": chunk,
                    "source": path.name,
                }
            )

    return documents