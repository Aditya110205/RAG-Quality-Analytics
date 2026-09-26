import time
import uuid
from datetime import datetime, timezone
import numpy as np

import duckdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from generator import MODEL_NAME, generate_answer
from retriever import retrieve
from logger import log_query


DB_PATH = "data/warehouse/analytics.duckdb"


app = FastAPI(
    title="RAG Quality Analytics API",
    description="API for the RAG Quality Analytics platform",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/query")
def query_rag(request: QueryRequest):
    query = request.query.strip()

    query_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        retrieval_start = time.perf_counter()
        chunks = retrieve(query, top_k=5)
        retrieval_latency_ms = (
            time.perf_counter() - retrieval_start
        ) * 1000

        if not chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found.",
            )

        generation_start = time.perf_counter()
        generation_result = generate_answer(query, chunks)
        generation_latency_ms = (
            time.perf_counter() - generation_start
        ) * 1000

        answer = generation_result["answer"]

        if not answer.strip():
            raise HTTPException(
                status_code=500,
                detail="LLM returned an empty answer.",
            )

        tokens_in = generation_result["tokens_in"]
        tokens_out = generation_result["tokens_out"]

        total_latency_ms = (
            retrieval_latency_ms + generation_latency_ms
        )

        event = {
            "query_id": query_id,
            "timestamp": timestamp,
            "query": query,
            "retrieved_chunks": len(chunks),
            "retrieval_latency_ms": round(
                retrieval_latency_ms, 2
            ),
            "generation_latency_ms": round(
                generation_latency_ms, 2
            ),
            "total_latency_ms": round(
                total_latency_ms, 2
            ),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "total_tokens": tokens_in + tokens_out,
            "cost_usd": 0.0,
            "answer": answer,
            "config": {
                "model": MODEL_NAME,
                "top_k": 5,
            },
        }

        log_query(event)

        return {
            "query_id": query_id,
            "answer": answer,
            "retrieved_chunks": len(chunks),
            "latency_ms": round(total_latency_ms, 2),
            "tokens": tokens_in + tokens_out,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline error: {exc}",
        ) from exc


@app.get("/metrics/daily")
def daily_metrics():
    try:
        con = duckdb.connect(DB_PATH, read_only=True)

        result = con.execute("""
            SELECT
            CAST(event_timestamp AS DATE) AS date,
    COUNT(*) AS query_count,
    ROUND(AVG(total_latency_ms), 2) AS avg_latency_ms,
    ROUND(
        MEDIAN(total_latency_ms), 2
    ) AS p50_latency_ms,
    ROUND(
        QUANTILE_CONT(total_latency_ms, 0.95), 2
    ) AS p95_latency_ms,
    ROUND(AVG(retrieval_latency_ms), 2)
        AS avg_retrieval_latency_ms,
    ROUND(AVG(generation_latency_ms), 2)
        AS avg_generation_latency_ms,
    ROUND(AVG(total_tokens), 2)
        AS avg_tokens,
    ROUND(AVG(cost_usd), 6)
        AS avg_cost_usd
    FROM fct_query_events
    GROUP BY 1
    ORDER BY 1
        """).fetchdf()

        con.close()

        return result.to_dict(orient="records")

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load daily metrics: {exc}",
        ) from exc


@app.get("/metrics/experiments")
def experiment_metrics():
    try:
        con = duckdb.connect(DB_PATH, read_only=True)

        result = con.execute("""
            SELECT *
            FROM agg_experiment_comparison
            ORDER BY experiment_id
        """).fetchdf()

        con.close()

        return result.to_dict(orient="records")

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load experiment metrics: {exc}",
        ) from exc
        
@app.get("/metrics/distribution")
def distribution_metrics(metric: str = "latency"):
    if metric != "latency":
        raise HTTPException(
            status_code=400,
            detail="Unsupported metric. Use metric=latency.",
        )

    try:
        con = duckdb.connect(DB_PATH, read_only=True)

        result = con.execute("""
            SELECT total_latency_ms
            FROM fct_query_events
            WHERE total_latency_ms IS NOT NULL
        """).fetchall()

        con.close()

        values = np.array([row[0] for row in result], dtype=float)

        if len(values) == 0:
            raise HTTPException(
                status_code=404,
                detail="No latency data available.",
            )

        return {
            "metric": metric,
            "count": int(len(values)),
            "mean": round(float(np.mean(values)), 2),
            "std": round(float(np.std(values)), 2),
            "p50": round(float(np.percentile(values, 50)), 2),
            "p95": round(float(np.percentile(values, 95)), 2),
            "p99": round(float(np.percentile(values, 99)), 2),
            "min": round(float(np.min(values)), 2),
            "max": round(float(np.max(values)), 2),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate distribution: {exc}",
        ) from exc