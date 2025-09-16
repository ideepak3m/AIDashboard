import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import plotly.express as px
import sqlite3
import json
import pprint

# --- Load API Key ---
load_dotenv()
API_KEY = os.getenv("GPT5NANO_API_KEY")

# --- Database Connection ---
conn = sqlite3.connect('db/company.db')

# --- Load Prompt and Schema ---
with open("app/assets/responsePrompt.txt", "r") as f:
    base_prompt = f.read()

with open("app/assets/schema.yaml.txt", "r") as f:
    schema = f.read()

# --- Setup Client ---
client = OpenAI(api_key=API_KEY)

# --- Streamlit Layout ---
st.set_page_config(page_title="AI Assistant", layout="wide")

with st.sidebar:
    st.header("🤖 AI Chatbot")
    user_input = st.text_area("Ask a business query:", height=200)
    submit = st.button("Generate")
    debug_mode = st.checkbox("🔧 Use Debug Mode (skip LLM)", value=False)

st.title("AI Insights Dashboard")

# --- Caching DB query execution ---
@st.cache_data
def run_query(sql_query: str):
    return pd.read_sql_query(sql_query, conn)

# --- MAIN EXECUTION ---
if submit and user_input:
    if debug_mode:
        # Debug mode: predefined SQL + summary
        sql_query = """
        SELECT cc.id AS customer_id, cc.name AS customer_name, cc.state AS state,
               SUM(so.total_amount) AS total_2024
        FROM salesOrder so
        JOIN customerCompany cc ON so.customer_id = cc.id
        WHERE so.order_date >= '2024-01-01' AND so.order_date < '2025-01-01'
        GROUP BY cc.id, cc.name, cc.state
        ORDER BY total_2024 DESC
        LIMIT 5;
        """
        summary = "Ferguson, Short and Lambert (BC) is the top customer in 2024..."
        financial_columns = []
    else:
        # --- Step 1: SQL Generation Prompt ---
        sql_prompt = f"""{base_prompt}

You are an assistant that generates SQL queries for a SQLite database.
Use the schema below to understand the tables and columns.

Schema:
{schema}

User Request:
{user_input}

Rules:
- Always use state/province short codes (e.g., "ON" not "Ontario", "BC" not "British Columbia").
- Respond ONLY with valid JSON in this exact format (no markdown, no explanation):
{{
  "sql": "SELECT ...",
  "financial_columns": ["list of result column aliases that represent currency values"]
}}
"""
        try:
            resp_sql = client.responses.create(
                model="gpt-5-nano",
                input=sql_prompt,
                max_output_tokens=2500
            )
            sql_output = resp_sql.output_text.strip() if hasattr(resp_sql, "output_text") else ""
            if not sql_output:
                st.error("❌ Model returned no SQL output.")
                st.code(pprint.pformat(resp_sql.dict()), language="python")
                st.stop()

            try:
                parsed_sql = json.loads(sql_output)
            except json.JSONDecodeError:
                st.error(f"❌ Invalid JSON:\n\n{sql_output}")
                st.stop()

            sql_query = parsed_sql.get("sql")
            financial_columns = parsed_sql.get("financial_columns", [])

            if not sql_query or not sql_query.strip().lower().startswith("select"):
                st.error("❌ Unsafe or missing SQL.")
                st.stop()

            # --- Step 2: Summarization Prompt ---
            df_preview = run_query(sql_query).head(20)
            summary_prompt = f"""
You are an assistant that summarizes SQL query results for business insights.

User Request:
{user_input}

SQL Query Executed:
{sql_query}

Query Results (first 20 rows):
{df_preview.to_json(orient="records")}

Task:
Summarize the results in 1 or 2 sentences, highlighting key insights.
"""
            resp_summary = client.responses.create(
                model="gpt-5-nano",
                input=summary_prompt,
                max_output_tokens=2500
            )
            summary = resp_summary.output_text.strip() if hasattr(resp_summary, "output_text") else ""

        except Exception as e:
            st.error(f"❌ API call failed: {e}")
            st.stop()

    # --- Run the query (cached) ---
    try:
        df = run_query(sql_query)
    except Exception as e:
        st.error(f"❌ SQL execution failed: {e}\n\nQuery: {sql_query}")
        st.stop()

    # ✅ Store results in session so they persist across reruns
    if not df.empty:
        st.session_state.df = df.copy()
        st.session_state.summary = summary
        st.session_state.financial_columns = financial_columns
    else:
        st.warning("Query returned no results.")

# --- DISPLAY SECTION ---
if "df" in st.session_state and not st.session_state.df.empty:
    # --- Summary ---
    st.subheader("📋 Summary")
    st.markdown(st.session_state.summary or "No summary generated.")

    # --- Table ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Table")
        df_display = st.session_state.df.copy()
        financial_columns = st.session_state.get("financial_columns", [])
        if not financial_columns:
            financial_columns = [col for col in df_display.columns if pd.api.types.is_float_dtype(df_display[col])]
        for col in financial_columns:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else x)
        st.dataframe(df_display)

    # --- Chart ---
    with col2:
        st.subheader("📈 Chart")
        df_chart = st.session_state.df.copy()
        float_cols = df_chart.select_dtypes(include="float").columns.tolist()
        text_cols = df_chart.select_dtypes(include="object").columns.tolist()

        if len(float_cols) == 1 and len(text_cols) == 1:
            x_col = text_cols[0]
            y_col = float_cols[0]
        else:
            st.markdown("🎛️ Choose chart columns:")
            x_col = st.selectbox("X-axis (Text)", options=text_cols, index=0, key="x_axis")
            y_col = st.selectbox("Y-axis (Numeric)", options=float_cols, index=0, key="y_axis")

        if x_col and y_col and x_col in df_chart.columns and y_col in df_chart.columns:
            try:
                df_chart[y_col] = df_chart[y_col].astype(float)
            except Exception:
                pass
            fig = px.bar(df_chart, x=x_col, y=y_col, title=f"{x_col} vs {y_col}", text_auto=True)
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Chart columns not valid or missing.")
else:
    st.info("Enter a query in the sidebar to get started.")
