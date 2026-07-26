from abc import ABC

from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger


class ErrorLogger(AbstractLogger, ABC):
    def __init__(self, level):
        super().__init__()
        self._level = level

    def write(self, message):
        print("Error Console::Logger: " + message)
