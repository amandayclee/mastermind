from abc import ABC, abstractmethod

class NumberGenerator(ABC):
    @abstractmethod
    def generate(self, config):
        pass