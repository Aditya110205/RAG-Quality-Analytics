import sys
import uuid
import time
from datetime import datetime, timezone

from generator import generate_answer, MODEL_NAME
from retriever import retrieve
from logger import log_query


def main():
    if len(sys.argv) < 2:
        print('Usage: python ask.py "your question"')
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip()

    if not query:
        print("Error: question cannot be empty.")
        sys.exit(1)

    query_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # Retrieval timing
        retrieval_start = time.perf_counter()

        chunks = retrieve(query, top_k=5)

        retrieval_latency_ms = (
            time.perf_counter() - retrieval_start
        ) * 1000

        if not chunks:
            print("No relevant documents found.")
            return

        print("\n=== Retrieved Context ===")

        for i, chunk in enumerate(chunks, start=1):
            print(f"\n[{i}] {chunk['source']}")
            print(chunk["text"])

        print("\n=== Answer ===")

        # Generation timing
        generation_start = time.perf_counter()

        generation_result = generate_answer(query, chunks)

        generation_latency_ms = (
            time.perf_counter() - generation_start
        ) * 1000

        answer = generation_result["answer"]
        tokens_in = generation_result["tokens_in"]
        tokens_out = generation_result["tokens_out"]

        if not answer.strip():
            print("LLM returned an empty answer.")
            return

        print(answer)

        total_latency_ms = (
            retrieval_latency_ms + generation_latency_ms
        )

        event = {
            "query_id": query_id,
            "timestamp": timestamp,
            "query": query,
            "retrieved_chunks": len(chunks),
            "retrieval_latency_ms": round(retrieval_latency_ms, 2),
            "generation_latency_ms": round(generation_latency_ms, 2),
            "total_latency_ms": round(total_latency_ms, 2),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "total_tokens": tokens_in + tokens_out,
            "cost_usd": 0.0,
            "answer": answer,
            "config": {
                "model": MODEL_NAME,
                "top_k": 5
            }
        }

        log_query(event)

    except Exception as exc:
        print(f"Pipeline error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()