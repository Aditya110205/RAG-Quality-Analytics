{{ config(materialized='view') }}

WITH source_data AS (
    SELECT *
    FROM read_json_auto(
        '{{ var("project_root") }}/logs/experiment_results.jsonl'
    )
)

SELECT
    CAST(query_id AS VARCHAR) AS query_id,
    CAST(timestamp AS TIMESTAMP) AS event_timestamp,
    CAST(experiment_id AS VARCHAR) AS experiment_id,
    CAST(query AS VARCHAR) AS query_text,

    CAST(chunk_size AS INTEGER) AS chunk_size,
    CAST(overlap_percent AS INTEGER) AS overlap_percent,
    CAST(top_k AS INTEGER) AS top_k,
    CAST(model AS VARCHAR) AS model,

    CAST(retrieved_chunks AS INTEGER) AS retrieved_chunks,

    CAST(retrieval_latency_ms AS DOUBLE) AS retrieval_latency_ms,
    CAST(generation_latency_ms AS DOUBLE) AS generation_latency_ms,
    CAST(total_latency_ms AS DOUBLE) AS total_latency_ms,

    CAST(tokens_in AS BIGINT) AS tokens_in,
    CAST(tokens_out AS BIGINT) AS tokens_out,
    CAST(total_tokens AS BIGINT) AS total_tokens,

    CAST(cost_usd AS DOUBLE) AS cost_usd,
    CAST(answer AS VARCHAR) AS answer

FROM source_data