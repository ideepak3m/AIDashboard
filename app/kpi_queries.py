kpi_queries = {
    "total_sales": "SELECT COUNT(*) AS total_sales FROM salesOrder;",
    "total_revenue": "SELECT ROUND(SUM(total_amount), 2) AS total_revenue FROM salesOrder;",
    "inventory_count": "SELECT COUNT(*) AS inventory_count FROM inventory;",
    "sales_by_customer": '''
        SELECT c.name AS customer_name, COUNT(s.id) AS sales_count, ROUND(SUM(s.total_amount), 2) AS total_revenue
        FROM salesOrder s
        JOIN customerCompany c ON s.customer_id = c.id
        GROUP BY c.id, c.name
        ORDER BY total_revenue DESC;
    ''',
    "inventory_by_brand_model": '''
        SELECT p.brand, p.model, COUNT(i.id) AS inventory_count
        FROM inventory i
        JOIN product p ON i.product_id = p.id
        GROUP BY p.brand, p.model
        ORDER BY p.brand, p.model;
    '''
}
