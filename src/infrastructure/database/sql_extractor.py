import pandas as pd
from sqlalchemy import create_engine
from core.interfaces.extractor import Extractor

class SQLEXTRACTOR(Extractor):

    def __init__(self, database_connection):
        self.database_connection = database_connection
        
        # We define the queries here. 
        # Added the 'vendor_report' query based on your table screenshots.
        self._Query_Book = {
            "customers": "SELECT customer_id, name, email FROM raw.customers",
            "orders": "SELECT order_id, customer_id, total FROM raw.orders",
            "products": "SELECT id, sku, price FROM inventory.products",
            "vendor_report": """
                SELECT 
                    v.id AS ID,
                    v.address AS ADDRESS,
                    v.payment_terms AS PAYMENT_TERM,
                    v.status AS STATUS,
                    v.total_orders AS TOTAL_ORDE,
                    v.sku AS SKU_CODE,
                    s.created_date AS ORDER_DAT,
                    pr.total_received AS RECEIVED_QUANTITY,
                    pr.total_damaged AS DAMAGE_QUANTITY,
                    s.estimated_arrival AS EXPECTED_DELIVERY_DAT,
                    pr.created_date AS RECIEVED_DATE
                FROM vendors v
                INNER JOIN shipments s ON v.id = s.vendor_id
                INNER JOIN partial_receipts pr ON s.purchase_order_id = pr.previous_purchase_order_id
            """
        }

    def extract(self):
        # 1. Get the query based on the source name
        query = self._Query_Book.get(self.database_connection.source_name)
        
        if not query:
            raise ValueError(f"No query found for source: {self.database_connection.source_name}")

        try:
            # 2. Use the database_connection (assuming it holds the engine or URL)
            # If database_connection.connection is a SQLAlchemy engine:
            df = pd.read_sql(query, self.database_connection.connection)
            return df
            
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None