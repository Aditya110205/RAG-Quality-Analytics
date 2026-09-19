import sys

from generator import generate_answer
from retriever import retrieve


def main():
    if len(sys.argv) < 2:
        print('Usage: python ask.py "your question"')
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip()

    if not query:
        print("Error: question cannot be empty.")
        sys.exit(1)

    try:
        chunks = retrieve(query, top_k=5)

        if not chunks:
            print("No relevant documents found.")
            return

        print("\n=== Retrieved Context ===")

        for i, chunk in enumerate(chunks, start=1):
            print(f"\n[{i}] {chunk['source']}")
            print(chunk["text"])

        print("\n=== Answer ===")

        answer = generate_answer(query, chunks)

        if not answer.strip():
            print("LLM returned an empty answer.")
            return

        print(answer)

    except Exception as exc:
        print(f"Pipeline error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()