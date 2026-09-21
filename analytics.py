from collections import Counter
import json
from pathlib import Path
from statistics import mean


LOG_FILE = Path("logs/queries.jsonl")


def load_events():
    events = []

    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    return events


def percentile(values, percentile):
    values = sorted(values)

    if not values:
        return 0.0

    index = (len(values) - 1) * percentile / 100

    lower = int(index)
    upper = min(lower + 1, len(values) - 1)

    weight = index - lower

    return values[lower] + (
        values[upper] - values[lower]
    ) * weight


def calculate_metrics(events):
    # Only use complete operational events
    valid_events = [
        event
        for event in events
        if "total_latency_ms" in event
        and "retrieval_latency_ms" in event
        and "generation_latency_ms" in event
    ]

    if not valid_events:
        return {
            "query_count": 0,
            "average_latency_ms": 0.0,
            "p50_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "average_retrieval_latency_ms": 0.0,
            "average_generation_latency_ms": 0.0,
            "average_tokens": 0.0,
            "average_cost_usd": 0.0,
        }

    latencies = [
        event["total_latency_ms"]
        for event in valid_events
    ]

    retrieval_latencies = [
        event["retrieval_latency_ms"]
        for event in valid_events
    ]

    generation_latencies = [
        event["generation_latency_ms"]
        for event in valid_events
    ]

    tokens = [
        event.get("total_tokens", 0)
        for event in valid_events
    ]

    costs = [
        event.get("cost_usd", 0.0)
        for event in valid_events
    ]

    return {
        "query_count": len(valid_events),

        "average_latency_ms": round(
            mean(latencies), 2
        ),

        "p50_latency_ms": round(
            percentile(latencies, 50), 2
        ),

        "p95_latency_ms": round(
            percentile(latencies, 95), 2
        ),

        "average_retrieval_latency_ms": round(
            mean(retrieval_latencies), 2
        ),

        "average_generation_latency_ms": round(
            mean(generation_latencies), 2
        ),

        "average_tokens": round(
            mean(tokens), 2
        ),

        "average_cost_usd": round(
            mean(costs), 6
        ),
    }


def configuration_metrics(events):
    valid_events = [
        event
        for event in events
        if "total_latency_ms" in event
    ]

    by_model = {}

    for event in valid_events:
        config = event.get("config", {})
        model = config.get("model", "unknown")

        if model not in by_model:
            by_model[model] = []

        by_model[model].append(event)

    print("\n=== BY MODEL ===")

    for model, model_events in by_model.items():
        latencies = [
            event["total_latency_ms"]
            for event in model_events
        ]

        costs = [
            event.get("cost_usd", 0.0)
            for event in model_events
        ]

        print(f"\nModel: {model}")
        print(f"Queries: {len(model_events)}")
        print(f"Average latency: {mean(latencies):.2f} ms")
        print(f"Average cost: {mean(costs):.6f}")


def daily_query_volume(events):
    valid_events = [
        event
        for event in events
        if "total_latency_ms" in event
    ]

    dates = [
        event["timestamp"][:10]
        for event in valid_events
    ]

    counts = Counter(dates)

    print("\n=== QUERY VOLUME BY DATE ===")

    for date, count in sorted(counts.items()):
        print(f"{date}: {count} queries")


def main():
    events = load_events()

    if not events:
        print("No events found.")
        return

    metrics = calculate_metrics(events)

    print("\n=== RAG OPERATIONAL ANALYTICS ===")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    configuration_metrics(events)
    daily_query_volume(events)


if __name__ == "__main__":
    main()