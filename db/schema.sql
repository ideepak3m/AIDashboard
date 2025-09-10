
CREATE TABLE IF NOT EXISTS customerCompany (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    phone TEXT,
    email TEXT,
    website TEXT
);


CREATE TABLE IF NOT EXISTS customerContact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    job_title TEXT,
    FOREIGN KEY (company_id) REFERENCES customerCompany (id)
);


CREATE TABLE IF NOT EXISTS supplierCompany (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    phone TEXT,
    email TEXT,
    website TEXT
);



CREATE TABLE IF NOT EXISTS supplierContact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    job_title TEXT,
    FOREIGN KEY (supplier_id) REFERENCES supplierCompany (id)
);



CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    category TEXT,
    description TEXT,
    MSRP NUMERIC(10,2)
);



CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    serial_number TEXT UNIQUE,
    purchase_date DATE,
    purchase_price NUMERIC(10,2),
    condition TEXT, -- e.g New, Used, Refurbished
    source TEXT, -- e.g Manufacturer, Wholesaler, Retailer
    price NUMERIC(10,2),
    location TEXT,
    FOREIGN KEY (product_id) REFERENCES product (id)
);


CREATE TABLE IF NOT EXISTS salesOrder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status TEXT, -- e.g Pending, Shipped, Delivered, Cancelled
    FOREIGN KEY (customer_id) REFERENCES customerCompany (id)
);


CREATE TABLE IF NOT EXISTS salesOrderItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    inventory_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    FOREIGN KEY (order_id) REFERENCES salesOrder (id),
    FOREIGN KEY (inventory_id) REFERENCES inventory (id)
);


CREATE TABLE IF NOT EXISTS purchaseOrder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    supplier_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status TEXT, -- e.g Pending, Received, Cancelled
    FOREIGN KEY (supplier_id) REFERENCES supplierCompany (id)
);
        

CREATE TABLE IF NOT EXISTS purchaseOrderItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    FOREIGN KEY (order_id) REFERENCES purchaseOrder (id),
    FOREIGN KEY (product_id) REFERENCES product (id)
);


CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    job_title TEXT
);
    

CREATE TABLE IF NOT EXISTS employeeRole (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    role TEXT NOT NULL, -- e.g Sales, Inventory Management, Purchasing
    FOREIGN KEY (employee_id) REFERENCES employee (id)
);


CREATE TABLE IF NOT EXISTS CompanyInfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    tax_id TEXT
);


