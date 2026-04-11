import pandas as pd
from core.interfaces.transformer import Transformer

class PANDASCLEANER(Transformer):

    # 1. FIXED TYPO: changed 'trasnform' to 'transform'
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # 2. FIXED INDENTATION: Everything inside 'try' must be indented
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")
            
            if data.empty:
                raise ValueError("Input DataFrame is empty")
            
            # Cleaning steps
            data = data.dropna()
            data = data.drop_duplicates()
            return data

        except ValueError as e:
            print(f"Validation Error: {e}")
            return pd.DataFrame() 
        except Exception as e:
            print(f"An error occurred during transformation: {e}")  
            return pd.DataFrame()
