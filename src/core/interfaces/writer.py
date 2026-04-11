from abc import ABC,abstractmethod
import pandas as pd

class Writer(ABC):
    @classmethod
    @abstractmethod
    def write(self,df:pd.DataFrame)->None:
        pass