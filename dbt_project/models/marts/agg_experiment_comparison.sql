{{ config(materialized='table') }}

SELECT
    experiment_id,
    chunk_size,
    overlap_percent,
    top_k,
    model,

    COUNT(*) AS query_count,

    ROUND(AVG(total_latency_ms), 2) AS avg_latency_ms,
    ROUND(quantile_cont(total_latency_ms, 0.95), 2) AS p95_latency_ms,

    ROUND(AVG(retrieval_latency_ms), 2) AS avg_retrieval_latency_ms,
    ROUND(AVG(generation_latency_ms), 2) AS avg_generation_latency_ms,

    ROUND(AVG(total_tokens), 2) AS avg_total_tokens,
    ROUND(AVG(cost_usd), 6) AS avg_cost_usd

FROM {{ ref('stg_experiment_results') }}

GROUP BY
    experiment_id,
    chunk_size,
    overlap_percent,
    top_k,
    model

ORDER BY experiment_id