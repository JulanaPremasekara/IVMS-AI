# improt pandas as pd
# from core.interfaces.extractor import Extractor

# class SQLEXTRACTOR(Extractor):

#     def __init__(self,database_connection):
#         self.database_connection = database_connection

#         _Query_Book ={
#                 "customers": "SELECT customer_id, name, email FROM raw.customers",
#         "orders": "SELECT order_id, customer_id, total FROM raw.orders",
#         "products": "SELECT id, sku, price FROM inventory.products"
#         }

#         query =self._Query_Book.get(self.database_connection.source_name)


#         # use pd.read_sql() method