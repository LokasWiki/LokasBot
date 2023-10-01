from abc import ABC

from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger


class ConsoleLogger(AbstractLogger, ABC):
    def __init__(self, level):
        super().__init__()
        self._level = level

    def write(self, message):
        # todo: add Timestamps, context, etc
        print("Standard Console::Logger: " + message)
