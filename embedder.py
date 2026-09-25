import chromadb
from sentence_transformers import SentenceTransformer

from chunker import load_documents


DB_PATH = "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"


def build_index(
    collection_name: str,
    chunk_size: int,
    overlap: int,
) -> int:

    documents = load_documents(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=collection_name
    )

    model = SentenceTransformer(MODEL_NAME)

    texts = [doc["text"] for doc in documents]
    ids = [doc["id"] for doc in documents]

    metadatas = [
        {"source": doc["source"]}
        for doc in documents
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return collection.count()


if __name__ == "__main__":
    count = build_index(
        collection_name="rag_documents",
        chunk_size=256,
        overlap=25,
    )

    print(f"Stored {count} chunks in Chroma.")