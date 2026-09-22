from pathlib import Path

from pyspark.sql import SparkSession


PROJECT_ROOT = Path(__file__).resolve().parent

PARQUET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "queries"
)


spark = (
    SparkSession.builder
    .appName("Verify-RAG-Parquet")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)


try:

    df = spark.read.parquet(
        str(PARQUET_PATH)
    )

    print("\n=== SCHEMA ===")
    df.printSchema()

    print("\n=== ROW COUNT ===")
    print(df.count())

    print("\n=== DATA ===")
    df.show(
        20,
        truncate=False
    )

    print("\n=== PARTITIONS ===")

    (
        df
        .groupBy("dt")
        .count()
        .orderBy("dt")
        .show()
    )

finally:

    spark.stop()