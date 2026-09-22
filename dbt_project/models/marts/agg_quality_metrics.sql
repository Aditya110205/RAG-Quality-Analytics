{{
    config(
        materialized='table'
    )
}}

SELECT
    dt,

    COUNT(*) AS query_count,

    COUNT(*) FILTER (
        WHERE invalid_query_id = TRUE
    ) AS invalid_query_count,

    COUNT(*) FILTER (
        WHERE invalid_timestamp = TRUE
    ) AS invalid_timestamp_count,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE invalid_query_id = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS invalid_query_rate,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE invalid_timestamp = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS invalid_timestamp_rate

FROM {{ ref('fct_query_events') }}

GROUP BY
    dt

ORDER BY
    dt