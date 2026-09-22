{{
    config(
        materialized='table'
    )
}}

SELECT
    ROW_NUMBER() OVER (
        ORDER BY model
    ) AS model_key,

    model AS model_name

FROM (
    SELECT DISTINCT
        NULLIF(TRIM(model), '') AS model
    FROM {{ ref('stg_queries') }}
)

WHERE model IS NOT NULL