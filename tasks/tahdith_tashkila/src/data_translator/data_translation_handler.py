from abc import abstractmethod, ABC


class DataTranslationHandler(ABC):
    @abstractmethod
    def translate(self, value):
        pass
