# RAG Quality Analytics

A local Retrieval-Augmented Generation (RAG) system extended into a **data engineering and analytics platform** for monitoring RAG usage, performance, cost, and data quality.

The project is developed incrementally:

**Week 1 → RAG MVP**
**Week 2 → Operational Analytics**
**Week 3 → RAG Quality Evaluation**
**Week 4 → Analytics Warehouse Pipeline**

---

# Week 1 — RAG MVP

The system:

1. Loads text documents
2. Splits documents into chunks
3. Generates embeddings using Sentence Transformers
4. Stores embeddings in Chroma
5. Retrieves relevant chunks
6. Sends retrieved context to a local LLM
7. Generates a grounded answer

## Week 1 Architecture

```text
data/*.txt
    ↓
chunker.py
    ↓
Sentence Transformers
    ↓
Chroma
    ↓
retriever.py
    ↓
Ollama
    ↓
Grounded Answer
```

---

# Week 2 — RAG Operational Analytics

Week 2 adds observability and operational analytics around the RAG pipeline.

The system tracks:

* Query ID
* Timestamp
* Query
* Retrieved chunks
* Retrieval latency
* Generation latency
* Total latency
* Input tokens
* Output tokens
* Total tokens
* Cost per query
* Model configuration
* Top-K configuration

## Analytics

The project calculates:

* Query count
* Average latency
* P50 latency
* P95 latency
* Average retrieval latency
* Average generation latency
* Average tokens per query
* Average cost per query
* Query volume by date
* Metrics by model configuration

## Week 2 Architecture

```text
                    ┌──────────────┐
                    │   User Query │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Retriever   │
                    └──────┬───────┘
                           ↓
                    Retrieval Latency
                           ↓
                    ┌──────────────┐
                    │ Local Ollama │
                    └──────┬───────┘
                           ↓
                    Generation Latency
                           ↓
                    ┌──────────────┐
                    │    Answer    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Logger     │
                    └──────┬───────┘
                           ↓
                  queries.jsonl
                           ↓
                  Analytics Dataset
                           ↓
                  Streamlit Dashboard
```

---

# Week 3 — RAG Quality Evaluation

Week 3 focuses on evaluating the quality of generated RAG answers and retrieval results.

Planned evaluation dimensions include:

* Faithfulness
* Answer relevance
* Context relevance
* Retrieval quality
* Groundedness

> Evaluation datasets and quality metrics are developed separately from the operational telemetry pipeline.

---

# Week 4 — Analytics Warehouse Pipeline

Week 4 transforms the project from a simple logging/dashboard system into a **local analytical data platform**.

The pipeline now uses:

* PySpark
* Parquet
* DuckDB
* dbt
* Streamlit

## Week 4 Data Engineering Pipeline

```text
Raw Query Logs
     │
     │ JSONL
     ▼
┌──────────────┐
│   PySpark    │
│              │
│ • Cleaning   │
│ • Validation │
│ • DQ checks  │
│ • Dedup      │
└──────┬───────┘
       │
       │ Partitioned Parquet
       ▼
┌──────────────┐
│    DuckDB    │
│   Warehouse  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     dbt      │
│              │
│  Staging     │
│  Fact        │
│  Dimensions  │
│  Marts       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Streamlit   │
│  Analytics   │
│  Dashboard   │
└──────────────┘
```

## PySpark Processing

The PySpark pipeline processes the raw JSONL query events and produces cleaned, partitioned Parquet data.

It handles:

* Schema normalization
* Query ID normalization
* Timestamp parsing
* Query text cleaning
* Retrieval latency
* Generation latency
* Total latency
* Token metrics
* Cost metrics
* Nested model configuration extraction
* Invalid query ID detection
* Invalid timestamp detection
* Duplicate query ID handling
* Date partitioning

### Output

```text
data/
└── processed/
    └── queries/
        ├── dt=2026-09-21/
        │   └── *.parquet
        └── ...
```

Parquet files are partitioned by:

```text
dt
```

---

# DuckDB Analytical Warehouse

The cleaned Parquet data is queried through DuckDB.

Warehouse location:

```text
data/warehouse/analytics.duckdb
```

DuckDB provides the local analytical storage layer without requiring a cloud warehouse.

---

# dbt Transformation Layer

dbt manages the SQL transformation layer inside the warehouse.

## Staging

```text
stg_queries
```

Provides a cleaned and standardized representation of the query events.

## Fact

```text
fct_query_events
```

Grain:

```text
1 row = 1 RAG query event
```

The fact table contains:

* Query ID
* Query text
* Event timestamp
* Latency metrics
* Token metrics
* Cost
* Model
* Top-K
* Configuration
* Data-quality flags
* Date partition

## Dimension

```text
dim_models
```

Contains distinct LLM models observed in the query events.

## Analytical Marts

### Daily Metrics

```text
agg_daily_metrics
```

Provides:

* Query count
* Average latency
* P50 latency
* P95 latency
* Average retrieval latency
* Average generation latency
* Average tokens
* Average cost

### Quality Metrics

```text
agg_quality_metrics
```

Provides data-quality measurements such as:

* Invalid query count
* Invalid timestamp count
* Invalid query rate
* Invalid timestamp rate

### Configuration Metrics

```text
agg_configuration_metrics
```

Provides metrics by:

* Model
* Top-K
* Query count
* Average latency
* P50 latency
* P95 latency
* Retrieval latency
* Generation latency
* Token usage
* Cost

---

# Data Quality

The pipeline explicitly handles data-quality problems instead of silently producing incorrect analytics.

Current checks include:

```text
Null query IDs
Invalid timestamps
Duplicate query IDs
Null required fields
```

dbt tests validate important warehouse constraints such as:

```text
not_null
unique
```

The Week 4 warehouse pipeline currently passes its configured dbt data-quality tests.

---

# Streamlit Analytics Dashboard

Streamlit acts as the **presentation layer**.

The dashboard reads analytical data from DuckDB/dbt rather than performing the primary warehouse transformations itself.

## Dashboard

The dashboard provides:

* Total queries
* Average latency
* P50 latency
* P95 latency
* Average cost
* Retrieval latency
* Generation latency
* Query volume
* Daily latency
* Model/configuration performance
* Data-quality metrics
* Query event logs

## Dashboard Architecture

```text
                 DuckDB
                    │
                    ▼
             dbt Analytical Marts
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Daily Metrics  Quality   Configuration
        │           │           │
        └───────────┼───────────┘
                    ▼
               Streamlit
                    │
                    ▼
             Analytics UI
```

This separation keeps the architecture clean:

```text
PySpark → Data Processing
DuckDB   → Analytical Storage
dbt      → Transformations
Streamlit → Visualization
```

---

# Project Structure

```text
RAG-Quality-Analytics/
│
├── data/
│   ├── *.txt
│   ├── processed/
│   │   └── queries/
│   │       └── dt=YYYY-MM-DD/
│   │           └── *.parquet
│   │
│   ├── quarantine/
│   │   └── queries/
│   │
│   └── warehouse/
│       └── analytics.duckdb
│
├── logs/
│   ├── queries.jsonl
│   └── analytics.csv
│
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   │
│   └── models/
│       ├── staging/
│       │   ├── stg_queries.sql
│       │   └── schema.yml
│       │
│       └── marts/
│           ├── fct_query_events.sql
│           ├── dim_models.sql
│           ├── agg_daily_metrics.sql
│           ├── agg_quality_metrics.sql
│           ├── agg_configuration_metrics.sql
│           └── schema.yml
│
├── frontend/
│   └── dashboard.py
│
├── chroma_db/
│
├── ask.py
├── chunker.py
├── create_docs.py
├── embedder.py
├── generator.py
├── retriever.py
├── logger.py
├── analytics.py
├── export_analytics.py
├── spark_job.py
├── verify_parquet.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Requirements

* Windows
* Python 3.13+
* Java 17+
* Ollama
* Chroma
* Sentence Transformers
* PySpark
* DuckDB
* dbt
* dbt-duckdb
* Streamlit
* Pandas

---

# Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Make sure Ollama is installed and the required local model is available.

---

# Run the RAG Pipeline

Ask a question from the terminal:

```powershell
python ask.py "What is Apache Spark?"
```

The system:

```text
Question
   ↓
Retrieve relevant chunks
   ↓
Generate grounded answer
   ↓
Log operational metrics
```

---

# Run the Data Engineering Pipeline

Process the raw query logs:

```powershell
python spark_job.py
```

This produces partitioned Parquet data under:

```text
data/processed/queries/
```

Run the dbt transformations:

```powershell
cd dbt_project
dbt run
```

Run the data-quality tests:

```powershell
dbt test
```

The resulting analytical warehouse is:

```text
data/warehouse/analytics.duckdb
```

---

# Run the Dashboard

From the project root:

```powershell
streamlit run frontend/dashboard.py
```

The dashboard reads analytical data from the DuckDB warehouse.

---

# Current Status

## Week 1 — RAG MVP

**Completed**

* Document ingestion
* Chunking
* Embeddings
* Chroma vector storage
* Retrieval
* Local LLM generation
* Grounded answers

## Week 2 — Operational Analytics

**Completed**

* Structured query logging
* Latency tracking
* Token tracking
* Cost tracking schema
* P50/P95 analytics
* Configuration analytics
* Analytics dataset
* Operational dashboard

## Week 3 — RAG Quality Evaluation

**In Progress / Planned**

* Evaluation dataset
* RAG quality metrics
* Faithfulness
* Answer relevance
* Context relevance
* Retrieval quality analysis
* Quality analytics dashboard

## Week 4 — Analytics Warehouse Pipeline

**Completed**

* PySpark JSONL processing
* Schema normalization
* Data-quality handling
* Duplicate handling
* Partitioned Parquet
* DuckDB warehouse
* dbt staging models
* dbt fact model
* dbt dimension model
* Daily analytical mart
* Quality analytical mart
* Configuration analytical mart
* dbt data-quality tests
* Streamlit → DuckDB integration

---

# Long-Term Goal

The long-term goal is to build a complete analytics platform for understanding RAG systems across:

```text
Usage
  ↓
Performance
  ↓
Cost
  ↓
Quality
  ↓
Experiments
```
The project starts with a local RAG pipeline and progressively adds the data and analytics layers required to understand **how the RAG system performs, how much it costs, and how accurately it answers questions**.

---

# Week 5 — RAG Experimentation

Week 5 introduced controlled experimentation to measure the impact of RAG configuration on system performance.

## Experiment Setup

| Variable | Values |
|---|---|
| Chunk Size | 256, 512, 1024 |
| Overlap | 10% |
| Top-K | 5 |
| Model | gemma3:latest |
| Queries / Configuration | 5 |
| Generation Cost | $0 (local Ollama) |

## Results

| Experiment | Chunk Size | Avg Latency | P95 Latency | Avg Tokens | Cost |
|---|---:|---:|---:|---:|---:|
| EXP_000 | 256 | 3879 ms | 11778 ms | 460.4 | $0 |
| EXP_002 | 512 | 1305 ms | 1760 ms | 460.4 | $0 |
| EXP_003 | 1024 | 1302 ms | 1820 ms | 464.2 | $0 |

## Findings

- 512 and 1024 chunk configurations produced nearly identical average latency.
- The 256 chunk configuration showed substantially higher average and P95 latency in this experiment.
- Increasing chunk size from 512 to 1024 provided little additional latency improvement.
- Token usage remained nearly constant across the three configurations.
- All experiments had zero generation cost because the system used a local Ollama model.
- The experiment used 5 queries per configuration, so results should be treated as an initial benchmark rather than a statistically generalizable conclusion.
- All three configurations used `top_k=5` and `overlap=10%`.
- RAGAS quality metrics were not included because no validated ground-truth evaluation dataset was available.

## Analytics Architecture

```text
RAG Experiment Runner
        ↓
experiment_results.jsonl
        ↓
dbt staging
        ↓
agg_experiment_comparison
        ↓
Streamlit Experiments
        ↓
Power BI Experiment Analytics

                    RAG APPLICATION

                          │
                          ▼

                    User Questions

                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          Retriever                Ollama
              │                       │
              └───────────┬───────────┘
                          ▼
                    Query Logger
                          │
                          ▼
                    queries.jsonl
                          │
                          ▼
                       PySpark
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Cleaning        DQ       Deduplication
             │
             ▼
       Partitioned Parquet
             │
             ▼
           DuckDB
             │
             ▼
            dbt
             │
       ┌─────┼──────┬──────────┐
       ▼     ▼      ▼          ▼
    Staging Fact Dimensions  Marts
                              │
                              ▼
                         Streamlit
                              │
                              ▼
                   RAG Analytics platform

## API Architecture

The project uses FastAPI as an analytics API layer between the Streamlit dashboard and the analytical warehouse for selected business-level metrics.

### Request Flow

Streamlit → FastAPI → DuckDB

FastAPI currently exposes:

- `GET /health`
- `POST /query`
- `GET /metrics/daily`
- `GET /metrics/experiments`
- `GET /metrics/distribution`

Streamlit uses the API for daily metrics and experiment analytics.

For detailed raw query events and lower-level analytical exploration, Streamlit continues to query DuckDB directly. This avoids adding unnecessary API endpoints for operations that are better handled directly in the analytical warehouse.

This hybrid architecture keeps the API focused on reusable application-level metrics while preserving efficient analytical access to DuckDB.



