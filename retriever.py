import chromadb


DB_PATH = "chroma_db"


def retrieve(
    query: str,
    top_k: int = 5,
    collection_name: str = "rag_documents",
) -> list[dict]:

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_collection(
        name=collection_name
    )

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    retrieved = []

    for i, document in enumerate(results["documents"][0]):
        retrieved.append(
            {
                "text": document,
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i],
            }
        )

    return retrieved