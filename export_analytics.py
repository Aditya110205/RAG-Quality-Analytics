import json
import csv
from pathlib import Path


LOG_FILE = Path("logs/queries.jsonl")
OUTPUT_FILE = Path("logs/analytics.csv")


def load_events():
    events = []

    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    return events


def export_events(events):

    valid_events = [
        event
        for event in events
        if "total_latency_ms" in event
    ]

    if not valid_events:
        print("No valid operational events found.")
        return

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []

    for event in valid_events:

        config = event.get("config", {})

        rows.append({
            "query_id": event["query_id"],
            "timestamp": event["timestamp"],
            "query": event["query"],
            "model": config.get("model"),
            "top_k": config.get("top_k"),

            "retrieved_chunks": event["retrieved_chunks"],

            "retrieval_latency_ms":
                event["retrieval_latency_ms"],

            "generation_latency_ms":
                event["generation_latency_ms"],

            "total_latency_ms":
                event["total_latency_ms"],

            "tokens_in":
                event.get("tokens_in", 0),

            "tokens_out":
                event.get("tokens_out", 0),

            "total_tokens":
                event.get("total_tokens", 0),

            "cost_usd":
                event.get("cost_usd", 0.0),
        })

    fieldnames = rows[0].keys()

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Exported {len(rows)} events "
        f"to {OUTPUT_FILE}"
    )


def main():

    events = load_events()

    if not events:
        print("No events found.")
        return

    export_events(events)


if __name__ == "__main__":
    main()