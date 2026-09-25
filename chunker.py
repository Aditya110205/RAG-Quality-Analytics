from pathlib import Path


DATA_DIR = Path("data")

CHUNK_SIZE = 256
OVERLAP = 25


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def load_documents(
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[dict]:

    documents = []

    for path in DATA_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")

        chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, chunk in enumerate(chunks):
            documents.append(
                {
                    "id": f"{path.stem}_{index}",
                    "text": chunk,
                    "source": path.name,
                }
            )

    return documents