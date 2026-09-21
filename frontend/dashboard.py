from pathlib import Path
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "logs" / "analytics.csv"


st.set_page_config(
    page_title="RAG Quality Analytics",
    layout="wide"
)


st.title("RAG Operational Analytics")
st.caption("Week 2 — Usage, Performance & Cost")


df = pd.read_csv(CSV_FILE)


# =========================
# KPI CARDS
# =========================

query_count = len(df)

avg_latency = df["total_latency_ms"].mean()

p50_latency = df["total_latency_ms"].quantile(0.50)

p95_latency = df["total_latency_ms"].quantile(0.95)

avg_retrieval = df["retrieval_latency_ms"].mean()

avg_generation = df["generation_latency_ms"].mean()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Queries",
    query_count
)

col2.metric(
    "Avg Latency",
    f"{avg_latency:.0f} ms"
)

col3.metric(
    "P50 Latency",
    f"{p50_latency:.0f} ms"
)

col4.metric(
    "P95 Latency",
    f"{p95_latency:.0f} ms"
)

col5.metric(
    "Avg Cost",
    f"${df['cost_usd'].mean():.6f}"
)


st.divider()


# =========================
# LATENCY BREAKDOWN
# =========================

st.subheader("Latency Breakdown")

latency_data = pd.DataFrame({
    "Metric": [
        "Retrieval",
        "Generation"
    ],
    "Latency (ms)": [
        avg_retrieval,
        avg_generation
    ]
})

st.bar_chart(
    latency_data.set_index("Metric")
)


# =========================
# QUERY VOLUME
# =========================

st.subheader("Query Volume")

df["date"] = pd.to_datetime(
    df["timestamp"]
).dt.date

daily_queries = (
    df.groupby("date")
    .size()
)

st.line_chart(daily_queries)


# =========================
# QUERY LATENCY
# =========================

st.subheader("Query Latency")

latency_chart = df[
    [
        "query_id",
        "total_latency_ms"
    ]
].set_index("query_id")

st.bar_chart(latency_chart)


# =========================
# CONFIGURATION
# =========================

st.subheader("Configuration")

config_summary = (
    df.groupby(["model", "top_k"])
    .agg(
        queries=("query_id", "count"),
        avg_latency_ms=("total_latency_ms", "mean"),
        avg_tokens=("total_tokens", "mean"),
        avg_cost_usd=("cost_usd", "mean")
    )
    .reset_index()
)

st.dataframe(
    config_summary,
    use_container_width=True
)


# =========================
# RAW DATA
# =========================

with st.expander("View Query Logs"):

    st.dataframe(
        df,
        use_container_width=True
    )