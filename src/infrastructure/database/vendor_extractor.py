import pandas as pd
from core.interfaces.extractor import Extractor


class DummyVendorExtractor(Extractor):
    def extract(self) -> pd.DataFrame:
        data = [
            {
                "ID": "VEN132",
                "ADDRESS": "Thailand",
                "PAYMENT_TERN": "COD",
                "STATUS": "Active",
                "TOTAL_ORDE": 208,
                "SKU_CODE": "INV-1S1FOSUY",
                "ORDER_DAT": "2025-06-20",
                "QUANTITY": 125,
                "RECEIVED_QUANTITY": 41,
                "DAMAGE_QUANTITY": 5,
                "EXPECTED_DELIVERY_DAT": "2025-08-01",
                "RECIEVED_DATE": "2025-08-01",
            },
            {
                "ID": "VEN205",
                "ADDRESS": "India",
                "PAYMENT_TERN": "Net30",
                "STATUS": "Active",
                "TOTAL_ORDE": 145,
                "SKU_CODE": "INV-3VXFWN1E",
                "ORDER_DAT": "2025-06-25",
                "QUANTITY": 75,
                "RECEIVED_QUANTITY": 70,
                "DAMAGE_QUANTITY": 2,
                "EXPECTED_DELIVERY_DAT": "2025-08-05",
                "RECIEVED_DATE": "2025-08-04",
            },
            {
                "ID": "VEN301",
                "ADDRESS": "Malaysia",
                "PAYMENT_TERN": "COD",
                "STATUS": "Inactive",
                "TOTAL_ORDE": 90,
                "SKU_CODE": "INV-9KLMPQ21",
                "ORDER_DAT": "2025-07-01",
                "QUANTITY": 40,
                "RECEIVED_QUANTITY": 38,
                "DAMAGE_QUANTITY": 1,
                "EXPECTED_DELIVERY_DAT": "2025-08-10",
                "RECIEVED_DATE": "2025-08-09",
            },
        ]
        return pd.DataFrame(data)