sales_manager_map = {
    "Sales by Customer": """
        SELECT 
            cc.name AS customer,
            SUM(so.total_amount) AS total_sales
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.name
        ORDER BY 
            total_sales DESC;
    """,

    "Sales by Product": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            SUM(soi.quantity * soi.unit_price) AS total_sales
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            product
        ORDER BY 
            total_sales DESC;
    """,

    "Sales by Region": """
        SELECT 
            cc.state AS region,
            SUM(so.total_amount) AS total_sales
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.state
        ORDER BY 
            total_sales DESC;
    """,

    "Top Selling Products": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            COUNT(soi.id) AS units_sold,
            SUM(soi.quantity * soi.unit_price) AS revenue
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            product
        ORDER BY 
            units_sold DESC
        LIMIT 10;
    """,

    "Product sales by Region": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            cc.state AS region,
            SUM(soi.quantity * soi.unit_price) AS total_sales
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            product, cc.state
        ORDER BY 
            total_sales DESC;
    """,

    "Inventory Available": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            COUNT(i.id) AS available_units,
            i.location
        FROM 
            inventory i
        JOIN 
            product p ON i.product_id = p.id
        GROUP BY 
            product, i.location
        ORDER BY 
            available_units ASC;
    """,

    "Revenue by Customer": """
        SELECT 
            cc.name AS customer,
            SUM(so.total_amount) AS revenue
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.name
        ORDER BY 
            revenue DESC;
    """,

    "Revenue by Product": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            SUM(soi.quantity * soi.unit_price) AS revenue
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            product
        ORDER BY 
            revenue DESC;
    """,

    "Revenue by Region": """
        SELECT 
            cc.state AS region,
            SUM(so.total_amount) AS revenue
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.state
        ORDER BY 
            revenue DESC;
    """,

    "Top Customers": """
        SELECT 
            cc.name AS customer,
            COUNT(so.id) AS orders,
            SUM(so.total_amount) AS total_spent
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.name
        ORDER BY 
            total_spent DESC
        LIMIT 10;
    """
}

ceo_map = {
    "Revenue Growth Overview": """
        SELECT 
            strftime('%Y-%m', order_date) AS month,
            SUM(total_amount) AS revenue
        FROM 
            salesOrder
        WHERE 
            strftime('%Y', order_date) = '{year}'
            AND strftime('%m', order_date) IN ({month_filter})
        GROUP BY 
            month
        ORDER BY 
            month ASC;
    """,

    "Quarterly Revenue Breakdown": """
        SELECT 
            CASE 
                WHEN strftime('%m', order_date) IN ('01','02','03') THEN 'Q1'
                WHEN strftime('%m', order_date) IN ('04','05','06') THEN 'Q2'
                WHEN strftime('%m', order_date) IN ('07','08','09') THEN 'Q3'
                WHEN strftime('%m', order_date) IN ('10','11','12') THEN 'Q4'
            END AS quarter,
            SUM(total_amount) AS revenue
        FROM 
            salesOrder
        WHERE 
            strftime('%Y', order_date) = '{year}'
            AND strftime('%m', order_date) IN ({month_filter})
        GROUP BY 
            quarter
        ORDER BY 
            quarter;
    """,

    "Revenue by Product Category": """
        SELECT 
            p.category,
            SUM(soi.quantity * soi.unit_price) AS revenue
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            p.category
        ORDER BY 
            revenue DESC;
    """,

    "Profit Margin by Product": """
        SELECT 
            p.brand || ' ' || p.model AS product,
            SUM(soi.quantity * soi.unit_price) AS revenue,
            SUM(soi.quantity * p.cost_price) AS cost,
            SUM(soi.quantity * soi.unit_price) - SUM(soi.quantity * p.cost_price) AS profit
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            product
        ORDER BY 
            profit DESC;
    """,

    "Gross Profit Trends": """
        SELECT 
            strftime('%Y-%m', so.order_date) AS month,
            SUM(soi.quantity * soi.unit_price) - SUM(soi.quantity * p.cost_price) AS gross_profit
        FROM 
            salesOrder so
        JOIN 
            salesOrderItem soi ON so.id = soi.order_id
        JOIN 
            inventory i ON soi.inventory_id = i.id
        JOIN 
            product p ON i.product_id = p.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            month
        ORDER BY 
            month ASC;
    """,

    "Customer Lifetime Value (CLV)": """
        SELECT 
            cc.name AS customer,
            COUNT(so.id) AS orders,
            SUM(so.total_amount) AS lifetime_value
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        GROUP BY 
            cc.name
        ORDER BY 
            lifetime_value DESC
        LIMIT 10;
    """,

    "Sales Forecast vs Actuals": """
        SELECT 
            f.month,
            f.forecast_amount,
            IFNULL(SUM(so.total_amount), 0) AS actual_sales
        FROM 
            forecast f
        LEFT JOIN 
            salesOrder so ON strftime('%Y-%m', so.order_date) = f.month
            AND strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        WHERE 
            strftime('%Y', f.month) = '{year}'
        GROUP BY 
            f.month
        ORDER BY 
            f.month ASC;
    """,

    "Top Performing Sales Regions": """
        SELECT 
            cc.state AS region,
            SUM(so.total_amount) AS revenue
        FROM 
            salesOrder so
        JOIN 
            customerCompany cc ON so.customer_id = cc.id
        WHERE 
            strftime('%Y', so.order_date) = '{year}'
            AND strftime('%m', so.order_date) IN ({month_filter})
        GROUP BY 
            cc.state
        ORDER BY 
            revenue DESC
        LIMIT 5;
    """,

    "Year-over-Year Revenue Comparison": """
        SELECT 
            strftime('%Y', order_date) AS year,
            SUM(total_amount) AS revenue
        FROM 
            salesOrder
        WHERE 
            strftime('%m', order_date) IN ({month_filter})
        GROUP BY 
            year
        ORDER BY 
            year ASC;
    """,

    "Quarter-over-Quarter Growth": """
        SELECT 
            CASE 
                WHEN strftime('%m', order_date) IN ('01','02','03') THEN 'Q1'
                WHEN strftime('%m', order_date) IN ('04','05','06') THEN 'Q2'
                WHEN strftime('%m', order_date) IN ('07','08','09') THEN 'Q3'
                WHEN strftime('%m', order_date) IN ('10','11','12') THEN 'Q4'
            END AS quarter,
            strftime('%Y', order_date) AS year,
            SUM(total_amount) AS revenue
        FROM 
            salesOrder
        WHERE 
            strftime('%Y', order_date) IN ('{year}', '{prev_year}')
            AND strftime('%m', order_date) IN ({month_filter})
        GROUP BY 
            year, quarter
        ORDER BY 
            year, quarter;
    """
}
