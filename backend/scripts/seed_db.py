# # scripts/seed_db.py

# import sqlite3

# conn = sqlite3.connect("db/crm.db")

# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS customers (
#     customer_id TEXT PRIMARY KEY,
#     name TEXT,
#     email TEXT,
#     order_id TEXT UNIQUE,
#     product_name TEXT,
#     product_type TEXT,
#     order_value REAL,
#     purchase_date TEXT,
#     delivery_date TEXT,
#     promised_delivery_date TEXT,
#     refund_count_last_12_months INTEGER,
#     already_refunded BOOLEAN,
#     item_condition TEXT,
#     fraud_flag BOOLEAN,
#     is_final_sale BOOLEAN,
#     subscription_renewal BOOLEAN,
#     renewal_date TEXT,
#     gift_purchase BOOLEAN,
#     exchange_completed BOOLEAN,
#     shipment_status TEXT
# )
# """)

# conn.commit()
# conn.close()

# print("Database created successfully.")









import sqlite3
import json

conn = sqlite3.connect("db/crm.db")

cursor = conn.cursor()

with open("data/customers_seed.json", "r") as f:
    customers = json.load(f)

for customer in customers:
    cursor.execute("""
    INSERT OR REPLACE INTO customers
    VALUES (
        :customer_id,
        :name,
        :email,
        :order_id,
        :product_name,
        :product_type,
        :order_value,
        :purchase_date,
        :delivery_date,
        :promised_delivery_date,
        :refund_count_last_12_months,
        :already_refunded,
        :item_condition,
        :fraud_flag,
        :is_final_sale,
        :subscription_renewal,
        :renewal_date,
        :gift_purchase,
        :exchange_completed,
        :shipment_status
    )
    """, customer)

conn.commit()
conn.close()

print("Customers inserted successfully.")