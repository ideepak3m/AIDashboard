
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from dashboard_queries import sales_manager_map, ceo_map


conn = sqlite3.connect('db/company.db')
report_df = pd.DataFrame()  # Initialize report_df

def get_month_filter(period, quarter=None, half=None):
    if period == "Quarter":
        quarter_map = {
            "Q1": ["01", "02", "03"],
            "Q2": ["04", "05", "06"],
            "Q3": ["07", "08", "09"],
            "Q4": ["10", "11", "12"]
        }
        return quarter_map.get(quarter, [])
    
    elif period == "Half-Year":
        half_map = {
            "H1": ["01", "02", "03", "04", "05", "06"],
            "H2": ["07", "08", "09", "10", "11", "12"]
        }
        return half_map.get(half, [])
    
    elif period == "Year":
        return [f"{i:02}" for i in range(1, 13)]

    return []




st.set_page_config(page_title="Company Dashboard", layout="wide")
st.title("Company Dashboard")

# Adding report options
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    period = st.radio("Period", ["Quarter", "Half-Year", "Year"], horizontal=True)

with row1_col2:
    quarter = None
    half = None
    if period == "Quarter":
        quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
    elif period == "Half-Year":
        half = st.selectbox("Half Year", ["H1", "H2"])
        
with row1_col3:
    year = st.selectbox("Year", list(range(2020, 2026)))

row2_col1, row2_col2, row2_col3 = st.columns(3)

    
with row2_col1:
    role = st.selectbox("Select Role", ["CEO", "Sales Manager"])

with row2_col2:
    report_options = {
    "Sales Manager": list(sales_manager_map.keys()),
    "CEO": list(ceo_map.keys())
    }
    report_type = st.selectbox("Select Report", report_options[role])


with row2_col3:
    if "report_df" not in st.session_state:
        st.session_state.report_df = pd.DataFrame()
    if st.button("Generate Report"):
        months = get_month_filter(period, quarter, half)
        month_filter = ",".join(f"'{m}'" for m in months)

        query_template = sales_manager_map[report_type] if role == "Sales Manager" else ceo_map[report_type]
        query = query_template.format(year=year, month_filter=month_filter)
        

        report_df = pd.read_sql_query(query, conn)
        # Identify financial columns
        financial_cols = ["total_sales", "revenue", "total_spent", "lifetime_value", "gross_profit", "profit", "cost"]

        # Format them as currency
        for col in financial_cols:
            if col in report_df.columns:
                report_df[col] = report_df[col].apply(lambda x: f"${x:,.2f}")
        report_df = report_df.reset_index(drop=True)
        report_df.index += 1      
        st.session_state.report_df = report_df
    
report_df = st.session_state.report_df   
# Layout for table and chart
if not report_df.empty:
    table_col, chart_col = st.columns([2, 3])

    with table_col:
        st.subheader("Report Table")
        # Replace this with your actual DataFrame
        st.dataframe(report_df)

    with chart_col:
        st.subheader("Report Chart")
        chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Pie"], key="chart_type")

        if len(report_df.columns) >= 2:
            label = report_df.columns[0]
            value = report_df.columns[1]

            if chart_type == "Bar":
                fig = px.bar(report_df, x=label, y=value, text=value, color=value, color_continuous_scale="Plasma")
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(
                    title="Bar Chart",
                    xaxis_title=label,
                    yaxis_title=value,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Line":
                fig = px.line(report_df, x=label, y=value, markers=True)
                fig.update_layout(
                    title="Line Chart",
                    xaxis_title=label,
                    yaxis_title=value,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Pie":
                fig = px.pie(report_df, names=label, values=value)
                fig.update_layout(
                    title="Pie Chart",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Not enough data to generate chart.")

else:
    st.info("Please select report parameters and click 'Generate Report' to view the report.")
