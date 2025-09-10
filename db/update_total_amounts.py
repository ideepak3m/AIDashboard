import sqlite3

conn = sqlite3.connect('db/company.db')
cursor = conn.cursor()

# Update total_amount columns to two decimal places
cursor.execute('UPDATE purchaseOrder SET total_amount = ROUND(total_amount, 2);')
cursor.execute('UPDATE salesOrder SET total_amount = ROUND(total_amount, 2);')

conn.commit()
conn.close()
