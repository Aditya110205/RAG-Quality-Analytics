import chromadb
from sentence_transformers import SentenceTransformer

from chunker import load_documents


COLLECTION_NAME = "rag_documents"
DB_PATH = "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    documents = load_documents()

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
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
        show_progress_bar=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Stored {collection.count()} chunks in Chroma.")


if __name__ == "__main__":
    main()