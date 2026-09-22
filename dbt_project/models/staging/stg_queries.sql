{{
    config(
        materialized='view'
    )
}}

WITH source_data AS (
    SELECT *
    FROM read_parquet(
        '{{ var("project_root") }}/data/processed/queries/**/*.parquet',
        hive_partitioning = true
    )
),

cleaned AS (
    SELECT
        -- Core Identifiers & Text
        CAST(query_id AS VARCHAR) AS query_id,
        NULLIF(TRIM(query_text), '') AS query_text,
        CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,

        -- Latency Metrics (ms)
        CAST(latency_ms AS DOUBLE) AS latency_ms,
        CAST(retrieval_latency_ms AS DOUBLE) AS retrieval_latency_ms,
        CAST(generation_latency_ms AS DOUBLE) AS generation_latency_ms,
        CAST(total_latency_ms AS DOUBLE) AS total_latency_ms,

        -- Token Counts
        CAST(tokens_in AS BIGINT) AS tokens_in,
        CAST(tokens_out AS BIGINT) AS tokens_out,
        CAST(total_tokens AS BIGINT) AS total_tokens,

        -- Cost
        CAST(cost_usd AS DOUBLE) AS cost_usd,

        -- Model & Configuration
        NULLIF(TRIM(model), '') AS model,
        CAST(top_k AS INTEGER) AS top_k,
        config_json,

        -- Data Quality Flags
        CAST(invalid_timestamp AS BOOLEAN) AS invalid_timestamp,
        CAST(invalid_query_id AS BOOLEAN) AS invalid_query_id,

        -- Partition Date
        CAST(dt AS DATE) AS dt

    FROM source_data
)

SELECT *
FROM cleaned