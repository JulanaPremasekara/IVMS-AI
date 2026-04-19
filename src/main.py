from config.settings import Settings
from infrastructure.database.inventory_extractor import  DummyInventoryExtractor
from infrastructure.database.vendor_extractor import DummyVendorExtractor
from infrastructure.database.sql_extractor import SQLEXTRACTOR
from infrastructure.transform.pandas_cleaner import PANDASCLEANER
from infrastructure.storage.csv_writer import  CSVWRITER
from infrastructure.tracking.dvc_tracker import DVCTRACKER
from use_case.run_etl import RunETLUseCase
from infrastructure.database.connection import MySQLConnection


def main():
    transformer = PANDASCLEANER()
    writer = CSVWRITER()
    tracker = DVCTRACKER()

    
    db_conn = MySQLConnection(
        uri=Settings.DATABASE_URL, 
        source_name="vendor_report"
    )
    
    vendor_extractor = SQLEXTRACTOR(database_connection=db_conn)
    inventory_extractor = DummyInventoryExtractor()

    vendor_use_case = RunETLUseCase(
        extractor=vendor_extractor,
        transformer=transformer,
        writer=writer,
        tracker=tracker,
    )

    inventory_use_case = RunETLUseCase(
        extractor=inventory_extractor,
        transformer=transformer,
        writer=writer,
        tracker=tracker,
    )

    vendor_use_case.execute(Settings.VENDOR_OUTPUT_PATH)
    inventory_use_case.execute(Settings.INVENTORY_OUTPUT_PATH)


if __name__ == "__main__":
    main()