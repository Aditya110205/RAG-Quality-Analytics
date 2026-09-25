# RAG Quality Analytics

A minimal local Retrieval-Augmented Generation (RAG) system built as the foundation for a **RAG Quality Analytics platform**.

The project is being developed incrementally:

**Week 1 → RAG MVP**
**Week 2 → Operational Analytics**
**Week 3 → RAG Quality Evaluation**

---

## Week 1 — RAG MVP

The system:

1. Loads text documents
2. Splits documents into chunks
3. Generates embeddings using Sentence Transformers
4. Stores embeddings in Chroma
5. Retrieves relevant chunks
6. Sends retrieved context to a local LLM
7. Generates a grounded answer

### Week 1 Architecture

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

## Week 2 — RAG Operational Analytics

Week 2 adds observability and operational analytics around the RAG pipeline.

The system now tracks:

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

### Analytics

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

### Week 2 Architecture

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
                    analytics.csv
                           ↓
                  Streamlit Dashboard
```

---

## Project Structure

```text
RAG-Quality-Analytics/
│
├── data/
│   └── *.txt
│
├── logs/
│   ├── queries.jsonl
│   └── analytics.csv
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
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Requirements

* Windows
* Python 3.13+
* Ollama
* Chroma
* Sentence Transformers
* Streamlit
* Pandas

---

## Setup

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

Make sure Ollama is installed and the required model is available.

---

## Run the RAG Pipeline

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

## Generate Analytics Dataset

After running queries:

```powershell
python export_analytics.py
```

This creates:

```text
logs/analytics.csv
```

---

## Run the Dashboard

Start Streamlit from the project root:

```powershell
streamlit run frontend/dashboard.py
```

The dashboard displays:

* Query count
* Average latency
* P50 latency
* P95 latency
* Average cost
* Retrieval vs generation latency
* Query volume
* Query latency
* Model/configuration metrics
* Query logs

---

## Current Status

### Week 1 — RAG MVP

**Completed**

* Document ingestion
* Chunking
* Embeddings
* Chroma vector storage
* Retrieval
* Local LLM generation
* Grounded answers

### Week 2 — Operational Analytics

**Completed**

* Structured query logging
* Latency tracking
* Token tracking
* Cost tracking schema
* P50/P95 analytics
* Configuration analytics
* Analytics CSV layer
* Streamlit operational dashboard

### Week 3 — RAG Quality Evaluation

**Next**

* Evaluation dataset
* RAGAS integration
* Faithfulness
* Answer relevance
* Context relevance
* Retrieval quality analysis
* Quality analytics dashboard

---

## Project Goal

The long-term goal is to build an analytics platform that evaluates a RAG system across:

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

## Week 5 — RAG Experimentation

Week 5 introduced controlled experimentation to measure the impact of RAG configuration on system performance.

### Experiment Setup

| Variable | Values |
|---|---|
| Chunk Size | 256, 512, 1024 |
| Overlap | 10% |
| Top-K | 5 |
| Model | gemma3:latest |
| Queries / Configuration | 5 |
| Generation Cost | $0 (local Ollama) |

### Results

| Experiment | Chunk Size | Avg Latency | P95 Latency | Avg Tokens | Cost |
|---|---:|---:|---:|---:|---:|
| EXP_000 | 256 | 3879 ms | 11778 ms | 460.4 | $0 |
| EXP_002 | 512 | 1305 ms | 1760 ms | 460.4 | $0 |
| EXP_003 | 1024 | 1302 ms | 1820 ms | 464.2 | $0 |

### Findings

- 512 and 1024 chunk configurations produced nearly identical average latency.
- The 256 chunk configuration showed substantially higher average and P95 latency in this experiment.
- Increasing chunk size from 512 to 1024 provided little additional latency improvement.
- Token usage remained nearly constant across the three configurations.
- All experiments had zero generation cost because the system used a local Ollama model.
- The experiment used 5 queries per configuration, so results should be treated as an initial benchmark rather than a statistically generalizable conclusion.
- RAGAS quality metrics were not included because no validated ground-truth evaluation dataset was available.

### Analytics Architecture

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