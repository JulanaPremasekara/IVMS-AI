import os
import pandas as pd
from core.interfaces.writer import Writer

class CSVWRITER(Writer):

    def write(self,data:pd.DataFrame,output_path:str) -> None:
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")
            
            if data.empty:
                raise ValueError("Input DataFrame is empty")
            
            dir_to_create = os.path.dirname(output_path)
            # Ensure the output directory exists
            if dir_to_create:
                os.makedirs(dir_to_create, exist_ok=True)
            
            # Write the DataFrame to a CSV file
            data.to_csv(output_path, index=False)
            print(f"Data successfully written to {output_path}")

        except ValueError as e:
            print(f"Validation Error: {e}") 
        except FileExistsError:
            print(f"File already exists at {output_path}. Please choose a different path or filename.")
        except PermissionError:
            print(f"Permission denied when trying to write to {output_path}. Please check your permissions.")
        except OSError as e:
            print(f"Error: The path '{dir_to_create}' is invalid or inaccessible. ({e})")
        except Exception as e:
            print(f"An error occurred while writing to CSV: {e}")