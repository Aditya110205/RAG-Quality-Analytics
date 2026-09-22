from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION & SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_FILE = (
    PROJECT_ROOT
    / "data"
    / "warehouse"
    / "analytics.duckdb"
)

st.set_page_config(
    page_title="RAG Quality Analytics",
    layout="wide"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    """Establish a cached, read-only connection to the DuckDB warehouse."""
    return duckdb.connect(
        str(DB_FILE),
        read_only=True
    )


con = get_connection()


# ============================================================
# LOAD ANALYTICAL MARTS
# ============================================================

daily_df = con.sql(
    """
    SELECT *
    FROM agg_daily_metrics
    ORDER BY dt
    """
).df()

quality_df = con.sql(
    """
    SELECT *
    FROM agg_quality_metrics
    ORDER BY dt
    """
).df()

config_df = con.sql(
    """
    SELECT *
    FROM agg_configuration_metrics
    ORDER BY query_count DESC
    """
).df()

query_df = con.sql(
    """
    SELECT
        query_id,
        query_text,
        event_timestamp,
        model,
        top_k,
        retrieval_latency_ms,
        generation_latency_ms,
        total_latency_ms,
        tokens_in,
        tokens_out,
        total_tokens,
        cost_usd,
        dt
    FROM fct_query_events
    ORDER BY event_timestamp DESC
    """
).df()


# ============================================================
# APP HEADER
# ============================================================

st.title("RAG Operational Analytics")
st.caption("Week 4 — PySpark → Parquet → dbt → DuckDB Pipeline Dashboard")

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_queries = len(query_df)
avg_latency = query_df["total_latency_ms"].mean()
p50_latency = query_df["total_latency_ms"].quantile(0.50)
p95_latency = query_df["total_latency_ms"].quantile(0.95)
avg_retrieval = query_df["retrieval_latency_ms"].mean()
avg_generation = query_df["generation_latency_ms"].mean()
avg_cost = query_df["cost_usd"].mean() if "cost_usd" in query_df.columns else float("nan")


# ============================================================
# KPI CARDS DISPLAY
# ============================================================

st.subheader("High-Level Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Queries", f"{total_queries:,}")
col2.metric("Avg Latency", f"{avg_latency:.0f} ms" if pd.notna(avg_latency) else "N/A")
col3.metric("P50 Latency", f"{p50_latency:.0f} ms" if pd.notna(p50_latency) else "N/A")
col4.metric("P95 Latency", f"{p95_latency:.0f} ms" if pd.notna(p95_latency) else "N/A")
col5.metric("Avg Cost", f"${avg_cost:.6f}" if pd.notna(avg_cost) else "N/A")

st.divider()


# ============================================================
# LATENCY BREAKDOWN & TRENDS
# ============================================================

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Latency Breakdown")
    latency_data = pd.DataFrame(
        {
            "Metric": ["Retrieval", "Generation"],
            "Latency (ms)": [avg_retrieval, avg_generation]
        }
    )
    st.bar_chart(latency_data.set_index("Metric"))

with col_right:
    st.subheader("Query Volume Trend")
    if not daily_df.empty:
        daily_volume = daily_df[["dt", "query_count"]].copy()
        daily_volume["dt"] = pd.to_datetime(daily_volume["dt"])
        st.line_chart(daily_volume.set_index("dt"))
    else:
        st.info("No daily metrics available.")


# ============================================================
# DAILY LATENCY TRENDS
# ============================================================

st.subheader("Daily Latency Trends")

if not daily_df.empty:
    daily_latency = daily_df[
        [
            "dt",
            "avg_latency_ms",
            "p50_latency_ms",
            "p95_latency_ms"
        ]
    ].copy()
    daily_latency["dt"] = pd.to_datetime(daily_latency["dt"])
    st.line_chart(daily_latency.set_index("dt"))
else:
    st.info("No latency data available.")


# ============================================================
# CONFIGURATION ANALYTICS
# ============================================================

st.subheader("Model & Configuration Performance")

if not config_df.empty:
    st.dataframe(config_df, use_container_width=True)
else:
    st.info("No configuration metrics available.")


# ============================================================
# DATA QUALITY MONITORING
# ============================================================

st.subheader("Data Quality Metrics")

if not quality_df.empty:
    latest_quality = quality_df.iloc[-1]

    q1, q2, q3 = st.columns(3)
    q1.metric("Invalid Queries", int(latest_quality["invalid_query_count"]))
    q2.metric("Invalid Query Rate", f"{latest_quality['invalid_query_rate']:.2f}%")
    q3.metric("Invalid Timestamp Rate", f"{latest_quality['invalid_timestamp_rate']:.2f}%")
else:
    st.info("No quality metrics available.")


# ============================================================
# RAW QUERY LOGS EXPANDER
# ============================================================

st.divider()

with st.expander("🔍 View Raw Query Events Explorer"):
    st.dataframe(query_df, use_container_width=True)