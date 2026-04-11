import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_URL = os.getenv("DB_URL")
    VENDOR_OUTPUT_PATH = os.getenv(
        "VENDOR_OUTPUT_PATH",
        "./vendor.csv"
    )

    INVENTORY_OUTPUT_PATH = os.getenv(
        "SALES_OUTPUT_PATH",
        "./inventory.csv"
    )


    # VENDOR_QUERY