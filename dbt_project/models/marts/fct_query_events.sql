{{
    config(
        materialized='table'
    )
}}

SELECT
    -- Core Identifiers & Text
    query_id,
    query_text,
    event_timestamp,

    -- Latency Metrics (ms)
    latency_ms,
    retrieval_latency_ms,
    generation_latency_ms,
    total_latency_ms,

    -- Token Counts
    tokens_in,
    tokens_out,
    total_tokens,

    -- Cost
    cost_usd,

    -- Model & Configuration
    model,
    top_k,
    config_json,

    -- Data Quality Flags
    invalid_timestamp,
    invalid_query_id,

    -- Partition Date
    dt

FROM {{ ref('stg_queries') }}

-- Exclude records with invalid query IDs from the final fact table
WHERE NOT invalid_query_id