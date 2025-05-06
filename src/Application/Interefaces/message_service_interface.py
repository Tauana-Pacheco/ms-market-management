from abc import ABC, abstractmethod

class IMessageService(ABC):
    @abstractmethod
    def send_message(self, number:str, message:str) -> str:
        pass