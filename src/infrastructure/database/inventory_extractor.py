import pandas as pd
from core.interfaces.extractor import Extractor


class DummyInventoryExtractor(Extractor):
    def extract(self) -> pd.DataFrame:
        data = [
            {
                "WAREHOUSE_LOCATION": "SEEDUWA",
                "IS_ACTIVE": "Yes",
                "CATEGORY_NAME": "Electronics",
                "SKU_CODE": "INV-3VXFWN1E",
                "UNIT_PRICE": 334549.74,
                "INITIAL_STOCK": 3078,
                "REORDER_THRESHOLD": 16,
            },
            {
                "WAREHOUSE_LOCATION": "COLOMBO",
                "IS_ACTIVE": "Yes",
                "CATEGORY_NAME": "Accessories",
                "SKU_CODE": "INV-1S1FOSUY",
                "UNIT_PRICE": 15499.50,
                "INITIAL_STOCK": 250,
                "REORDER_THRESHOLD": 20,
            },
            {
                "WAREHOUSE_LOCATION": "KANDY",
                "IS_ACTIVE": "No",
                "CATEGORY_NAME": "Furniture",
                "SKU_CODE": "INV-9KLMPQ21",
                "UNIT_PRICE": 45200.00,
                "INITIAL_STOCK": 18,
                "REORDER_THRESHOLD": 10,
            },
        ]
        return pd.DataFrame(data)