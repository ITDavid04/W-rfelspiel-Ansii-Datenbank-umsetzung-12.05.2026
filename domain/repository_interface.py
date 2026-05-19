from abc import ABC, abstractmethod

class WuerfelRepository(ABC):
    @abstractmethod
    def save(self, data: dict):
        pass