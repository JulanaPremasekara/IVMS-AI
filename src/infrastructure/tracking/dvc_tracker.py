from core.interfaces.tracker import Tracker

class DVCTRACKER(Tracker):

    def track(self, file_path: str) -> None:
        try:
            if not isinstance(file_path, str):
                raise ValueError("Input file path must be a string")

            # Simulate tracking by printing the file path
            print(f"Tracking file: {file_path}")

        except ValueError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"An error occurred during tracking: {e}")
