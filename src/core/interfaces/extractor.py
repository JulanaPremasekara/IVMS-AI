from abc import ABC,abstractmethod
import pandas as pd

class Extractor(ABC):
    @classmethod
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        pass

