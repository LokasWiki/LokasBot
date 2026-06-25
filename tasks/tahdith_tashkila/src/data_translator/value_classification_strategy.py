from abc import abstractmethod, ABC


class ValueClassificationStrategy(ABC):
    @abstractmethod
    def classify(self, value):
        pass
