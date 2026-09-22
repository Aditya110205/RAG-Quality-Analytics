from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_ROOT / "data" / "warehouse" / "analytics.duckdb"


def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB database not found: {DATABASE_PATH}"
        )

    con = duckdb.connect(str(DATABASE_PATH), read_only=True)

    try:
        print("\n=== DATABASE ===")
        print(DATABASE_PATH)

        print("\n=== TABLES / VIEWS ===")
        print(con.sql("SHOW TABLES"))

        print("\n=== STG_QUERIES SCHEMA ===")
        print(con.sql("DESCRIBE stg_queries"))

        print("\n=== ROW COUNT ===")
        print(
            con.sql(
                "SELECT COUNT(*) AS row_count FROM stg_queries"
            )
        )

        print("\n=== SAMPLE DATA ===")
        print(
            con.sql(
                """
                SELECT
                    query_id,
                    query_text,
                    event_timestamp,
                    latency_ms,
                    model,
                    dt
                FROM stg_queries
                ORDER BY event_timestamp
                LIMIT 10
                """
            )
        )

    finally:
        con.close()


if __name__ == "__main__":
    main()