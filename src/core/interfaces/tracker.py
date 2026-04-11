from abc import ABC,abstractmethod

class Tracker(ABC):
    @classmethod
    @abstractmethod
    def track(self,file_path:str)->None:
        pass