import sqlite3

conn = sqlite3.connect('db\company.db')
cursor = conn.cursor()

with open('db/schema.sql', 'r') as f:
    sql = f.read()

cursor.executescript(sql)

conn.commit()
conn.close()