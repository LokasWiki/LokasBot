from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

    _level = None
    # next element in chain or responsibility
    _nextLogger = None

    @property
    def nextLogger(self):
        return self._nextLogger

    @nextLogger.setter
    def nextLogger(self, value):
        self._nextLogger = value

    def logMessage(self, level, message):
        if self._level <= level:
            self.write(message)
        if self._nextLogger is not None:
            self._nextLogger.logMessage(level, message)

    @abstractmethod
    def write(self, message):
        pass
