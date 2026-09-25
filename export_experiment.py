import duckdb

DB_PATH = "data/warehouse/analytics.duckdb"
OUTPUT_PATH = "data/experiment_comparison.csv"

con = duckdb.connect(DB_PATH, read_only=True)

con.execute(f"""
    COPY (
        SELECT *
        FROM agg_experiment_comparison
    )
    TO '{OUTPUT_PATH}'
    (HEADER, DELIMITER ',')
""")

con.close()

print(f"Exported: {OUTPUT_PATH}")