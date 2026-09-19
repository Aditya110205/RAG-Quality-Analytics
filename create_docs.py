from pathlib import Path


DOCS = {
    "airflow.txt": """
Apache Airflow is an open-source platform for orchestrating workflows.
It represents workflows as directed acyclic graphs called DAGs.
A DAG contains tasks and defines dependencies between those tasks.

Airflow is commonly used for batch data pipelines.
Tasks can run Python code, execute shell commands, transfer data,
or interact with external systems.

Airflow supports scheduling, retries, logging, monitoring, and task dependencies.
It is useful when a data pipeline needs reliable orchestration.
""",

    "aws_s3.txt": """
Amazon S3 is an object storage service provided by AWS.
S3 stores data as objects inside buckets.

S3 is commonly used as a data lake storage layer.
Data engineers can store CSV, JSON, Parquet, images, logs, and other files in S3.

S3 provides high durability and scalable storage.
Applications can access S3 through APIs, SDKs, command-line tools,
and AWS services.
""",

    "aws_glue.txt": """
AWS Glue is a managed data integration service.
It can discover, transform, and move data between different systems.

Glue Data Catalog stores metadata about datasets.
Glue jobs can run Apache Spark-based ETL workloads.

AWS Glue is commonly used for serverless ETL pipelines
and integration with services such as S3 and Redshift.
""",

    "aws_redshift.txt": """
Amazon Redshift is a cloud data warehouse provided by AWS.
It is designed for analytical workloads involving large datasets.

Redshift uses column-oriented storage and massively parallel processing.
It can query structured data using SQL.

Data engineers commonly load data from S3 into Redshift
for analytics and business intelligence workloads.
""",

    "chromadb.txt": """
Chroma is an open-source vector database designed for AI applications.
It can store embeddings together with associated documents and metadata.

Vector databases allow applications to search for semantically similar content.
A query is converted into an embedding and compared with stored embeddings.

Chroma can be used to build retrieval systems for RAG applications.
""",

    "data_lake.txt": """
A data lake is a storage system designed to hold large amounts of raw
and processed data in its original or near-original format.

Data lakes commonly store structured, semi-structured, and unstructured data.
Object storage such as Amazon S3 is frequently used to implement data lakes.

Data lakes provide flexible storage and are often used before
data is transformed for analytical workloads.
""",

    "data_warehouse.txt": """
A data warehouse is a centralized system optimized for analytical queries.
It typically stores structured and transformed business data.

Data warehouses commonly use fact and dimension tables.
They support reporting, dashboards, aggregation, and business intelligence.

Examples include Snowflake, Amazon Redshift, and Google BigQuery.
""",

    "dbt.txt": """
dbt is a transformation tool used in modern data platforms.
It allows data teams to transform data using SQL inside a warehouse.

dbt supports models, tests, documentation, and dependency management.
Models can be organized into staging, intermediate, and mart layers.

dbt is commonly used after raw data has been loaded into a warehouse.
""",

    "docker.txt": """
Docker is a platform for packaging applications and their dependencies
inside containers.

A Docker image contains the files and dependencies required to run an application.
A container is a running instance of an image.

Docker helps create consistent environments across development,
testing, and production systems.
""",

    "etl.txt": """
ETL stands for Extract, Transform, Load.
The process extracts data from source systems, transforms the data,
and loads the result into a destination system.

Transformation can include cleaning data, changing data types,
removing duplicates, and applying business rules.

ETL pipelines are common in traditional data engineering architectures.
""",

    "kafka.txt": """
Apache Kafka is a distributed event streaming platform.
It allows applications to publish and consume streams of records.

Kafka organizes records into topics.
Producers write messages to topics and consumers read messages from topics.

Kafka is commonly used for real-time data pipelines,
event-driven architectures, and streaming analytics.
""",

    "parquet.txt": """
Apache Parquet is a columnar storage file format.
It is designed for efficient analytical workloads.

Parquet stores data by columns rather than by rows.
This can reduce the amount of data read when a query only needs
specific columns.

Parquet also supports compression and efficient encoding.
It is widely used in data lake and Spark-based architectures.
""",

    "postgresql.txt": """
PostgreSQL is an open-source relational database management system.
It supports SQL, transactions, indexes, constraints, and complex queries.

PostgreSQL is commonly used for transactional applications,
data services, and analytical workloads involving moderate datasets.

It supports advanced features such as window functions,
common table expressions, JSON data, and extensions.
""",

    "pyspark.txt": """
PySpark is the Python API for Apache Spark.
It allows Python applications to process large datasets using Spark.

PySpark DataFrames provide a structured interface for transformations
and analytical operations.

PySpark is commonly used for batch ETL, data cleaning,
large-scale transformations, and data lake processing.
""",

    "python.txt": """
Python is a general-purpose programming language widely used in data engineering.
It provides libraries for data processing, APIs, automation, testing,
and pipeline development.

Common Python libraries in data engineering include Pandas,
Requests, PySpark, SQLAlchemy, and boto3.

Python is often used to connect different systems and implement
data transformation or orchestration logic.
""",

    "rag.txt": """
Retrieval-Augmented Generation, or RAG, combines information retrieval
with large language model generation.

A RAG system first retrieves relevant documents or chunks.
Those retrieved chunks are then provided to an LLM as context.

The model generates an answer using the supplied context.
This can reduce the need for the model to rely only on its
pretrained knowledge.
""",

    "sql.txt": """
SQL is a language used to query and manipulate relational data.
It supports operations such as SELECT, INSERT, UPDATE, and DELETE.

SQL queries can filter, aggregate, join, and sort data.
Window functions can calculate values across related rows
without collapsing the result into groups.

SQL is one of the most important tools in data engineering
and analytical workloads.
""",

    "spark.txt": """
Apache Spark is a distributed data processing framework.
It can process large datasets across multiple machines.

Spark provides APIs for batch processing, SQL, streaming,
machine learning, and graph processing.

Spark transformations are generally evaluated lazily.
This allows Spark to optimize execution before running the computation.
""",

    "snowflake.txt": """
Snowflake is a cloud-based data platform designed for data warehousing
and analytical workloads.

Snowflake separates compute and storage.
Organizations can create different virtual warehouses
for different workloads.

Snowflake supports SQL, semi-structured data, data sharing,
and scalable analytical processing.
""",

    "airflow_monitoring.txt": """
Airflow monitoring helps data engineers identify failed or slow tasks.
The Airflow user interface provides information about DAG runs,
task states, logs, and execution history.

Retries can automatically rerun failed tasks.
Alerts can notify engineers when important workflows fail.

Monitoring is important because production data pipelines
need visibility into failures and operational performance.
"""
}


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

for filename, content in DOCS.items():
    path = DATA_DIR / filename
    path.write_text(content.strip(), encoding="utf-8")

print(f"Created {len(DOCS)} documents in {DATA_DIR}")