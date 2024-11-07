import sqlite3
import json
from JSON_data_1 import get_store_items


item_dict = get_store_items('No Frills')

conn = sqlite3.connect('No_Frills.db')

#create a cursor
cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS noFrills""")
cursor.execute("""CREATE TABLE IF NOT EXISTS noFrills (url text, product_name text, price float, stock text)""")

for url, item in item_dict.items():
    cursor.execute("INSERT INTO noFrills VALUES (?, ?, ?, ?)", [url, item['product_name'], item['price'], item['stock']])
    conn.commit()

cursor.execute("SELECT * FROM noFrills")
items = cursor.fetchall()

for item in items:
    print(item)

conn.close()