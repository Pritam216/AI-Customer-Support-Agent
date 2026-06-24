from langchain.tools import tool
import sqlite3

@tool
def crm_lookup(order_id: str):
    """
    Fetch customer order information from CRM database.
    """    
    conn = sqlite3.connect("db/crm.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM customers WHERE order_id=?",
        (order_id,)
    )

    row = cursor.fetchone()
    conn.close()
    if not row:
        return "Order not found"
    # return dict(row)
    return (
        f"Order ID: {row['order_id']}, "
        f"Product: {row['product_name']}, "
        f"Type: {row['product_type']}, "
        f"Condition: {row['item_condition']}"
    )