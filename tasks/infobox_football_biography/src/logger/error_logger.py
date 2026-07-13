from tasks.infobox_football_biography.src.logger.abstract_logger import AbstractLogger


class ErrorLogger(AbstractLogger):
    def __init__(self, level):
        super().__init__()
        self._level = level

    def write(self, message):
        print("Error Console::Logger: " + message)
