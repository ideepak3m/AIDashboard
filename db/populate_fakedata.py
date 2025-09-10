import datetime


from asyncio.windows_events import NULL
from faker import Faker
import random
import sqlite3
import pandas as pd

fake = Faker('en_CA')
conn = sqlite3.connect('db/company.db')
cursor = conn.cursor()

""" # Drop and recreate supplierContact table to use supplier_id
cursor.execute('DROP TABLE IF EXISTS supplierContact;')
cursor.execute('''
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
''') """

# Customers

cities_states = {
    'Toronto': 'ON',
    'Vancouver': 'BC',
    'Montreal': 'QC',
    'Calgary': 'AB',
    'Ottawa': 'ON',
    'Edmonton': 'AB',
    'Winnipeg': 'MB',
    'Quebec City': 'QC',
    'Hamilton': 'ON',
    'Kitchener': 'ON'
}

# Delete all existing data
""" cursor.execute('DELETE FROM customerCompany;')

for _ in range(100):
    name = fake.company()
    address = fake.street_address()
    city = random.choice(list(cities_states.keys()))
    state = cities_states[city]
    zip_code = fake.postalcode()
    phone = fake.phone_number()
    email = fake.company_email()
    website = fake.url()
    cursor.execute(
        'INSERT INTO customerCompany (name, address, city, state, zip_code, phone, email, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (name, address, city, state, zip_code, phone, email, website)
    )
 """    

# customercontacts
job_titles = ['CEO', 'Accountant', 'Manager', 'Sales Representative', 'Engineer', 'HR Specialist', 'Marketing Director']
              
cursor.execute('SELECT id FROM customerCompany')
company_ids = [row[0] for row in cursor.fetchall()]

for company_id in company_ids:
    #CEO
    cursor.execute('INSERT INTO customerContact(company_id, first_name, last_name, job_title, email, phone) VALUES (?, ?, ?, ?, ?, ?)',
                   (company_id, fake.first_name(), fake.last_name(), 'CEO', fake.email(), fake.phone_number())
    )
    #Accountant
    cursor.execute('INSERT INTO customerContact(company_id, first_name, last_name, job_title, email, phone) VALUES (?,?,?,?,?,?)',
                   (company_id, fake.first_name(), fake.last_name(), 'Accountant', fake.email(), fake.phone_number())
    )
    #Random other contact
    other_title = random.choice([title for title in job_titles if title not in ['CEO','Accountant']])
    cursor.execute('INSERT INTO customerContact(company_id, first_name, last_name, job_title, email, phone) VALUES (?,?,?,?,?,?)',
                   (company_id, fake.first_name(), fake.last_name(), other_title, fake.email(), fake.phone_number())
    )   
    
# Suppliers
cursor.execute('DELETE FROM supplierCompany;')

for _ in range(15):
    name = fake.company()
    address = fake.street_address()
    city = random.choice(list(cities_states.keys()))
    state = cities_states[city]
    zip_code = fake.postalcode()
    phone = fake.phone_number()
    email = fake.company_email()
    website = fake.url()
    cursor.execute(
        'INSERT INTO supplierCompany (name, address, city, state, zip_code, phone, email, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (name, address, city, state, zip_code, phone, email, website)
    )
    
# suppliercontacts
cursor.execute('SELECT id FROM supplierCompany')
supplier_ids = [row[0] for row in cursor.fetchall()]

for supplier_id in supplier_ids:
    cursor.execute('INSERT INTO supplierContact(supplier_id, first_name, last_name, job_title, email, phone) VALUES (?,?,?,?,?,?)',
                   (supplier_id, fake.first_name(), fake.last_name(), 'Contact', fake.email(), fake.phone_number())
    )
    
# Products
cursor.execute('DELETE FROM product;')
brands = ['Canon', 'Ricoh', 'Xerox', 'HP']

models = {
    'Canon': ['X500', 'C3500', 'IR-ADV'],
    'Ricoh': ['Pro C7200', 'MP C4504', 'SP 8400'],
    'Xerox': ['AltaLink C8030', 'VersaLink B7030'],
    'HP': ['LaserJet MFP M528', 'PageWide Pro 577']
}

# Clear product table
cursor.execute('DELETE FROM product;')

years = list(range(2020, 2026))
categories = ['Printer', 'Copier', 'MFP', 'Scanner']

for brand, model_list in models.items():
    for model in model_list:
        for year in years:
            full_model = f"{brand} {model} {year}"
            category = random.choice(categories)
            msrp = round(random.uniform(8000, 15000), 2)
            description = fake.sentence(nb_words=10)
            cursor.execute(
                'INSERT INTO product (brand, model, category, description, MSRP) VALUES (?, ?, ?, ?, ?)',
                (brand, full_model, category, description, msrp)
            )
            

# Inventory
cursor.execute('DELETE FROM inventory;')

# Get all product ids and models
cursor.execute('SELECT id, model FROM product')
products = cursor.fetchall()

# New inventory: 2025 and 2026 models, 50-100 units each
for product in products:
    product_id, model = product
    if model.endswith('2025') or model.endswith('2026'):
        num_new = random.randint(50, 100)
        for _ in range(num_new):
            serial_number = fake.unique.bothify(text='SN-########')
            # For new inventory, purchase_date within last year
            today = datetime.date.today()
            one_year_ago = today.replace(year=today.year - 1)
            purchase_date = fake.date_between(start_date=one_year_ago, end_date=today)
            purchase_price = round(random.uniform(8000, 15000), 2)
            condition = 'New'
            source = 'Wholesaler'
            price = purchase_price
            location = random.choice(list(cities_states.keys()))
            cursor.execute(
                'INSERT INTO inventory (product_id, serial_number, purchase_date, purchase_price, condition, source, price, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (product_id, serial_number, purchase_date, purchase_price, condition, source, price, location)
            )

# Lease returns: 2020-2024 models, 20-40 units each, Used or Refurbished, Lease Returns, 30% discount
for product in products:
    product_id, model = product
    for yr in range(2020, 2025):
        if model.endswith(str(yr)):
            num_lease = random.randint(20, 40)
            for _ in range(num_lease):
                serial_number = fake.unique.bothify(text='LR-########')
                # Lease period: 3-5 years
                lease_years = random.randint(3, 5)
                # For lease returns, purchase_date between lease_years ago and lease_years-1 ago
                today = datetime.date.today()
                start = today.replace(year=today.year - lease_years)
                end = today.replace(year=today.year - (lease_years - 1))
                purchase_date = fake.date_between(start_date=start, end_date=end)
                purchase_price = round(random.uniform(8000, 15000), 2)
                price = round(purchase_price * 0.7, 2)
                condition = random.choice(['Used', 'Refurbished'])
                source = 'Lease Returns'
                location = random.choice(list(cities_states.keys()))
                cursor.execute(
                    'INSERT INTO inventory (product_id, serial_number, purchase_date, purchase_price, condition, source, price, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (product_id, serial_number, purchase_date, purchase_price, condition, source, price, location)
                )

# --- Purchase Orders and Purchase Order Items ---

# Clear tables
cursor.execute('DELETE FROM purchaseOrderItem;')
cursor.execute('DELETE FROM purchaseOrder;')

# 1. Historical purchase orders for years not in inventory (e.g., 2018, 2019)
historical_years = [2018, 2019]
for year in historical_years:
    for _ in range(10):  # 10 orders per year
        supplier_id = random.choice(supplier_ids)
        order_date = fake.date_between(start_date=datetime.date(year, 1, 1), end_date=datetime.date(year, 12, 31))
        order_number = f"PO{year}{fake.unique.random_int(1000,9999)}"
        status = random.choice(['Received', 'Cancelled'])
        total_amount = 0
        cursor.execute(
            'INSERT INTO purchaseOrder (order_number, supplier_id, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
            (order_number, supplier_id, order_date, 0, status)
        )
        order_id = cursor.lastrowid
        # Add 1-3 items per order
        for _ in range(random.randint(1, 3)):
            product_id = random.choice([p[0] for p in products])
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(8000, 15000), 2)
            total_amount += quantity * unit_price
            cursor.execute(
                'INSERT INTO purchaseOrderItem (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                (order_id, product_id, quantity, unit_price)
            )
        # Update total_amount
        cursor.execute('UPDATE purchaseOrder SET total_amount = ? WHERE id = ?', (total_amount, order_id))

# 2. Purchase orders/items matching inventory
cursor.execute('SELECT id, product_id, purchase_price, purchase_date FROM inventory')
inventory_items = cursor.fetchall()
for inv in inventory_items:
    inv_id, product_id, purchase_price, purchase_date = inv
    supplier_id = random.choice(supplier_ids)
    order_number = f"INVPO{inv_id}"
    status = 'Received'
    # Create or get purchase order for this date/supplier
    cursor.execute(
        'INSERT INTO purchaseOrder (order_number, supplier_id, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
        (order_number, supplier_id, purchase_date, purchase_price, status)
    )
    order_id = cursor.lastrowid
    # Each inventory item is a single item in the order
    cursor.execute(
        'INSERT INTO purchaseOrderItem (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
        (order_id, product_id, 1, purchase_price)
    )



# --- Sales Orders and Sales Order Items ---

# Clear tables
cursor.execute('DELETE FROM salesOrderItem;')
cursor.execute('DELETE FROM salesOrder;')

# Get all customer ids
cursor.execute('SELECT id FROM customerCompany')
all_customer_ids = [row[0] for row in cursor.fetchall()]

# Select 15 high value customers
high_value_customers = random.sample(all_customer_ids, 15)

# Get all inventory items with product category (id, product_id, condition, price, purchase_date, category)
cursor.execute('''
    SELECT inventory.id, inventory.product_id, inventory.condition, inventory.price, inventory.purchase_date, product.category
    FROM inventory
    JOIN product ON inventory.product_id = product.id
''')
inventory_items = cursor.fetchall()

years = list(range(2020, 2026))
statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']

# Helper: assign at least 3-4 orders per year to 50% of customers
regular_customers = random.sample([cid for cid in all_customer_ids if cid not in high_value_customers], k=int(0.5*len(all_customer_ids)))
for customer_id in regular_customers:
    for year in years:
        num_orders = random.randint(3, 4)
        for _ in range(num_orders):
            order_date = fake.date_between(start_date=datetime.date(year, 1, 1), end_date=datetime.date(year, 12, 31))
            order_number = f'SO{customer_id}{year}{fake.unique.random_int(1000,9999)}'
            status = random.choice(statuses)
            total_amount = 0
            cursor.execute(
                'INSERT INTO salesOrder (order_number, customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
                (order_number, customer_id, order_date, 0, status)
            )
            order_id = cursor.lastrowid
            # 1-3 items per order
            for _ in range(random.randint(1, 3)):
                inv = random.choice(inventory_items)
                inventory_id, _, condition, price, _, _ = inv
                quantity = random.randint(1, 2)
                unit_price = price
                total_amount += quantity * unit_price
                cursor.execute(
                    'INSERT INTO salesOrderItem (order_id, inventory_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                    (order_id, inventory_id, quantity, unit_price)
                )
            cursor.execute('UPDATE salesOrder SET total_amount = ? WHERE id = ?', (total_amount, order_id))

# High value customers: buy every month, bulk, with discounts
for customer_id in high_value_customers:
    for year in years:
        for month in range(1, 13):
            order_date = fake.date_between(start_date=datetime.date(year, month, 1), end_date=datetime.date(year, month, 28))
            order_number = f'HVSO{customer_id}{year}{month:02d}{fake.unique.random_int(1000,9999)}'
            status = random.choice(statuses)
            total_amount = 0
            cursor.execute(
                'INSERT INTO salesOrder (order_number, customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
                (order_number, customer_id, order_date, 0, status)
            )
            order_id = cursor.lastrowid
            # 3-6 items per order, copiers only (category is 'Copier' or 'MFP')
            for _ in range(random.randint(3, 6)):
                copier_inventory = [i for i in inventory_items if i[5] in ('Copier', 'MFP')]
                if copier_inventory:
                    inv = random.choice(copier_inventory)
                else:
                    inv = random.choice(inventory_items)
                inventory_id, _, condition, price, _, _ = inv
                quantity = random.randint(1, 5)
                # Discount: 10% off for new, 5% off for lease returns
                if condition == 'New':
                    unit_price = round(price * 0.9, 2)
                else:
                    unit_price = round(price * 0.95, 2)
                total_amount += quantity * unit_price
                cursor.execute(
                    'INSERT INTO salesOrderItem (order_id, inventory_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                    (order_id, inventory_id, quantity, unit_price)
                )
            cursor.execute('UPDATE salesOrder SET total_amount = ? WHERE id = ?', (total_amount, order_id))

# Other random sales orders for the rest
for _ in range(200):
    customer_id = random.choice(all_customer_ids)
    order_date = fake.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date(2025, 12, 31))
    order_number = f'RANDSO{customer_id}{fake.unique.random_int(1000,9999)}'
    status = random.choice(statuses)
    total_amount = 0
    cursor.execute(
        'INSERT INTO salesOrder (order_number, customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
        (order_number, customer_id, order_date, 0, status)
    )
    order_id = cursor.lastrowid
    for _ in range(random.randint(1, 3)):
        inv = random.choice(inventory_items)
        inventory_id, _, condition, price, _, _ = inv
        quantity = random.randint(1, 2)
        unit_price = price
        total_amount += quantity * unit_price
        cursor.execute(
            'INSERT INTO salesOrderItem (order_id, inventory_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
            (order_id, inventory_id, quantity, unit_price)
        )
    cursor.execute('UPDATE salesOrder SET total_amount = ? WHERE id = ?', (total_amount, order_id))
    
## --- Create one customer profile with 5 employees and roles ---
# Create a new customer
customer_name = "Demo Customer Inc."
address = fake.street_address()
city = random.choice(list(cities_states.keys()))
state = cities_states[city]
zip_code = fake.postalcode()
phone = fake.phone_number()
email = fake.company_email()
website = fake.url()
cursor.execute(
    'INSERT INTO customerCompany (name, address, city, state, zip_code, phone, email, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
    (customer_name, address, city, state, zip_code, phone, email, website)
)
demo_customer_id = cursor.lastrowid

# Create 5 employees for this customer
employee_roles = [
    ("Admin", "admin"),
    ("Sales Manager", "sales"),
    ("Inventory Specialist", "inventory"),
    ("Purchasing Agent", "purchasing"),
    ("Support Lead", "support")
]
employee_ids = []
for job_title, role in employee_roles:
    first_name = fake.first_name()
    last_name = fake.last_name()
    emp_email = fake.email()
    emp_phone = fake.phone_number()
    cursor.execute(
        'INSERT INTO employee (first_name, last_name, email, phone, job_title) VALUES (?, ?, ?, ?, ?)',
        (first_name, last_name, emp_email, emp_phone, job_title)
    )
    emp_id = cursor.lastrowid
    employee_ids.append(emp_id)
    cursor.execute(
        'INSERT INTO employeeRole (employee_id, role) VALUES (?, ?)',
        (emp_id, role)
    )

conn.commit()
conn.close()