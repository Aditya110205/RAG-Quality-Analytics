from ollama import chat


MODEL_NAME = "gemma3:latest"


def generate_answer(query: str, chunks: list[dict]) -> dict:
    context = "\n\n".join(
        f"Source: {chunk['source']}\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""
Answer the question using ONLY the context below.

If the context does not contain the answer, say:
"I don't know based on the provided documents."

Do not use outside knowledge.

Context:
{context}

Question:
{query}
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return {
        "answer": response["message"]["content"],
        "tokens_in": response.get("prompt_eval_count", 0),
        "tokens_out": response.get("eval_count", 0),
    }