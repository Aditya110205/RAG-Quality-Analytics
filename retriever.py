import chromadb


DB_PATH = "chroma_db"
COLLECTION_NAME = "rag_documents"


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_collection(
        name=COLLECTION_NAME
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


if __name__ == "__main__":
    results = retrieve("What is Apache Spark?")

    for i, result in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {result['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"])