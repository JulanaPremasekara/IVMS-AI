from core.interfaces.extractor import Extractor
from core.interfaces.transformer import Transformer
from core.interfaces.writer import Writer
from core.interfaces.tracker import Tracker


class RunETLUseCase:
    def __init__(
        self,
        extractor: Extractor,
        transformer: Transformer,
        writer: Writer,
        tracker: Tracker,
    ):
        self.extractor = extractor
        self.transformer = transformer
        self.writer = writer
        self.tracker = tracker

    def execute(self, output_path: str) -> None:
        try:
            print(" ETL process started")

            # --- Extract ---
            print(" Extracting data...")
            df = self.extractor.extract()
            print(f" Extraction completed. Rows fetched: {len(df)}")

            # --- Transform ---
            print(" Transforming data...")
            clean_df = self.transformer.transform(df)
            print(f" Transformation completed. Rows after cleaning: {len(clean_df)}")

            # --- Load ---
            print(" Writing data to CSV...")
            self.writer.write(clean_df, output_path)
            print(f" Data saved to {output_path}")

            # --- Track ---
            print(" Tracking output file...")
            self.tracker.track(output_path)
            print(" Tracking completed")

            print(" ETL process completed successfully!")

        except Exception as error:
            print("ETL process failed!")
            print(f"Error: {error}")
            raise