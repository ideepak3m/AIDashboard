
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from kpi_queries import kpi_queries
import chatbot

conn = sqlite3.connect('db/company.db')
#*****************************
# Initialize chatbot (if needed)
with st.sidebar:
    st.header("Chat with the Data")
    user_input = st.text_area("Ask a question about your data:", height=300)
    run_query = st.button("Get Answer")
        
        
if run_query and user_input:
    sql, display, chart_type = chatbot.get_chatbot_response(user_input)
    
    st.markdown("### :green[Chatbot Generated SQL:]")
    st.code(sql, language='sql')
    
    result_pf = pd.read_sql_query(sql, conn)
    
    if display == "summary":
        st.success(result_pf.iloc[0, 0])
    elif display == "table":
        st.dataframe(result_pf, use_container_width=True)
        fig = px.bar(result_pf, x=result_pf.columns[0], y=result_pf.columns[1], title="Bar Chart")
        st.plotly_chart(fig, use_container_width=True)

#*****************************




st.set_page_config(page_title="Company Dashboard", layout="wide")
st.title("Company Dashboard")

# Add custom CSS for purple border around KPI cards
st.markdown(
    """
    <style>
    .kpi-card {
        border: 2px solid purple;
        border-radius: 10px;
        padding: 0;
        margin-bottom: 0;
        background: #fff;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .element-container:has(.kpi-card) {
        padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# KPI cards
kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    total_sales = pd.read_sql_query(kpi_queries["total_sales"], conn).iloc[0, 0]
    st.markdown("### :orange[Total Sales]")
    st.metric(label="", value=total_sales)
    st.markdown('</div>', unsafe_allow_html=True)


with kpi2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    total_revenue = pd.read_sql_query(kpi_queries["total_revenue"], conn).iloc[0, 0]
    st.markdown("### :orange[Total Revenue]")
    st.metric(label="", value=f"${total_revenue:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)


with kpi3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    inventory_count = pd.read_sql_query(kpi_queries["inventory_count"], conn).iloc[0, 0]
    st.markdown("### :orange[Inventory Count]")
    st.metric(label="", value=inventory_count)
    st.markdown('</div>', unsafe_allow_html=True)


# --- New row: 2 columns for table and chart ---
st.write("")
row1_col1, row1_col2 = st.columns(2)

# Top 10 customers by value and machines bought in the current year
import datetime
current_year = datetime.date.today().year
sales_by_customer_year_query = f'''
    SELECT c.name AS Name,
           COUNT(soi.id) AS Units_Purchased,
           ROUND(SUM(so.total_amount), 2) AS Value
    FROM salesOrder so
    JOIN customerCompany c ON so.customer_id = c.id
    JOIN salesOrderItem soi ON soi.order_id = so.id
    WHERE strftime('%Y', so.order_date) = '{current_year}'
    GROUP BY c.id, c.name
    ORDER BY Value DESC
    LIMIT 10;
'''
top_customers = pd.read_sql_query(sales_by_customer_year_query, conn)

# Format currency for display
top_customers["Value"] = top_customers["Value"].apply(lambda x: f"${x:,.2f}")
    
# --- Row 1: Table and Chart ---
with row1_col1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown(f"### :orange[Top 10 Customers ({current_year})]")
    st.markdown('</div>', unsafe_allow_html=True)

    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=["Customer", "Units Purchased", "Total Value (CAD)"],
            fill_color='#333333',  # dark header
            font=dict(color='white', size=14),
            align='left',
            line_color='black'
        ),
        cells=dict(
            values=[top_customers[col] for col in top_customers.columns],
            fill_color=[['#1e1e1e', '#2a2a2a'] * (len(top_customers) // 2)],  # alternating dark rows
            font=dict(color='white', size=11),
            align='left',
            line_color='black'
        )
    )])
    st.markdown(f""" <div style="padding-right:20px;"> """, unsafe_allow_html=True)
    st.plotly_chart(fig_table, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown(f"### :blue[Customer Value Breakdown ({current_year})]")
    st.markdown('</div>', unsafe_allow_html=True)

    fig_bar = px.bar(
        top_customers,
        x="Name",
        y="Value",
        title="Top Customers by Purchase Value",
        labels={"Value": "Total Value", "Name": "Customer"},
        text="Value",
        color="Name"
    )
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig_bar, use_container_width=True)
    
# --- Row 2: Inventory by Brand/Model ---
inventory_by_brand_model_query = '''
    SELECT p.brand, p.model, COUNT(i.id) AS inventory_count
    FROM inventory i
    JOIN product p ON i.product_id = p.id
    GROUP BY p.brand, p.model
    ORDER BY p.brand, p.model;
'''

inventory_df = pd.read_sql_query(inventory_by_brand_model_query, conn)

row2_col1, row2_col2 = st.columns(2)

# --- Column 1: Bar Chart ---
with row2_col1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown(f"### :orange[Inventory by Brand/Model]")
    st.markdown('</div>', unsafe_allow_html=True)
    
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=["Brand", "Model", "Inventory"],
            fill_color='#333333',
            font=dict(color='white', size=14),
            align='left'
        ),
        cells=dict(
            values=[inventory_df[col] for col in inventory_df.columns],
            fill_color=[['#1e1e1e', '#2a2a2a'] * (len(inventory_df) // 2)],
            font=dict(color='white', size=11),
            align='left'
        )
    )])
    st.markdown(f""" <div style="padding-right:20px;"> """, unsafe_allow_html=True)
    st.plotly_chart(fig_table, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)



# --- Column 2: Styled Table ---
with row2_col2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown("### :blue[Inventory by Brand/Model]")
    st.markdown('</div>', unsafe_allow_html=True)

    fig_inventory = px.bar(
        inventory_df,
        x="model",
        y="inventory_count",
        color="brand",
        text="inventory_count",
        title="Inventory Distribution",
        labels={"inventory_count": "Units", "model": "Model"},
    )
    fig_inventory.update_traces(textposition='outside')
    fig_inventory.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig_inventory, use_container_width=True)
    