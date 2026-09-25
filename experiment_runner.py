import json
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass

from embedder import build_index
from generator import generate_answer, MODEL_NAME
from retriever import retrieve


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_id: str
    chunk_size: int
    overlap_percent: int
    top_k: int
    model: str = "gemma3:latest"


BASELINE = ExperimentConfig(
    experiment_id="EXP_000",
    chunk_size=256,
    overlap_percent=10,
    top_k=5,
)


EXPERIMENTS = [
    BASELINE,
    ExperimentConfig(
        experiment_id="EXP_002",
        chunk_size=512,
        overlap_percent=10,
        top_k=5,
    ),
    ExperimentConfig(
        experiment_id="EXP_003",
        chunk_size=1024,
        overlap_percent=10,
        top_k=5,
    ),
]


def validate_config(config: ExperimentConfig) -> None:
    if config.chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if not 0 <= config.overlap_percent < 100:
        raise ValueError("overlap_percent must be between 0 and 99")

    if config.top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    if not config.experiment_id:
        raise ValueError("experiment_id cannot be empty")

    if not config.model:
        raise ValueError("model cannot be empty")


RESULTS_FILE = Path("logs/experiment_results.jsonl")


def overlap_words(chunk_size: int, overlap_percent: int) -> int:
    return round(chunk_size * overlap_percent / 100)


def run_experiment(config: ExperimentConfig, queries: list[str]) -> None:
    validate_config(config)
    collection_name = f"experiment_{config.experiment_id}"

    overlap = overlap_words(
        config.chunk_size,
        config.overlap_percent,
    )

    print(f"\n=== {config.experiment_id} ===")
    print(
        f"chunk_size={config.chunk_size}, "
        f"overlap={overlap}, "
        f"top_k={config.top_k}"
    )

    count = build_index(
        collection_name=collection_name,
        chunk_size=config.chunk_size,
        overlap=overlap,
    )

    print(f"Indexed {count} chunks.")

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULTS_FILE.open("a", encoding="utf-8") as file:
        for query in queries:
            query_id = str(uuid.uuid4())

            start = time.perf_counter()

            chunks = retrieve(
                query,
                top_k=config.top_k,
                collection_name=collection_name,
            )

            retrieval_latency_ms = (
                time.perf_counter() - start
            ) * 1000

            if not chunks:
                continue

            generation_start = time.perf_counter()

            result = generate_answer(
                query,
                chunks,
            )

            generation_latency_ms = (
                time.perf_counter() - generation_start
            ) * 1000

            event = {
                "query_id": query_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "experiment_id": config.experiment_id,
                "query": query,
                "chunk_size": config.chunk_size,
                "overlap_percent": config.overlap_percent,
                "top_k": config.top_k,
                "model": MODEL_NAME,
                "retrieved_chunks": len(chunks),
                "retrieval_latency_ms": round(
                    retrieval_latency_ms, 2
                ),
                "generation_latency_ms": round(
                    generation_latency_ms, 2
                ),
                "total_latency_ms": round(
                    retrieval_latency_ms
                    + generation_latency_ms,
                    2,
                ),
                "tokens_in": result["tokens_in"],
                "tokens_out": result["tokens_out"],
                "total_tokens": (
                    result["tokens_in"]
                    + result["tokens_out"]
                ),
                "cost_usd": 0.0,
                "answer": result["answer"],
            }

            file.write(json.dumps(event) + "\n")

            print(
                f"{config.experiment_id} | "
                f"{query_id[:8]} | "
                f"{event['total_latency_ms']} ms"
            )


def main() -> None:
    queries = [
        "What is Apache Spark?",
        "What is Apache Airflow?",
        "What is Amazon S3?",
        "What is dbt?",
        "What is Apache Kafka?",
    ]

    for config in EXPERIMENTS:
        run_experiment(config, queries)


if __name__ == "__main__":
    main()