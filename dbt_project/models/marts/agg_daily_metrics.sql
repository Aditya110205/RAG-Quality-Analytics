{{
    config(
        materialized='table'
    )
}}

SELECT
    -- Dimension / Partition Date
    dt,

    -- Volume Metrics
    COUNT(*) AS query_count,

    -- Latency Metrics (ms)
    ROUND(AVG(total_latency_ms), 2) AS avg_latency_ms,
    ROUND(QUANTILE_CONT(total_latency_ms, 0.50), 2) AS p50_latency_ms,
    ROUND(QUANTILE_CONT(total_latency_ms, 0.95), 2) AS p95_latency_ms,
    ROUND(AVG(retrieval_latency_ms), 2) AS avg_retrieval_latency_ms,
    ROUND(AVG(generation_latency_ms), 2) AS avg_generation_latency_ms,

    -- Token Metrics
    ROUND(AVG(total_tokens), 2) AS avg_total_tokens,

    -- Cost Metrics
    ROUND(AVG(cost_usd), 6) AS avg_cost_usd

FROM {{ ref('fct_query_events') }}

GROUP BY
    dt

ORDER BY
    dt