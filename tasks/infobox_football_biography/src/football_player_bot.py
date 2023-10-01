from tasks.infobox_football_biography.src.logger.abstract_logger import AbstractLogger
from tasks.infobox_football_biography.src.logger.console_logger import ConsoleLogger
from tasks.infobox_football_biography.src.logger.error_logger import ErrorLogger
from tasks.infobox_football_biography.src.logger.file_logger import FileLogger


class FootballPlayerBot:

    def getChainOfLoggers(self) -> AbstractLogger:
        errorLogger = ErrorLogger(AbstractLogger.ERROR)
        fileLogger = FileLogger(AbstractLogger.DEBUG)
        consoleLogger = ConsoleLogger(AbstractLogger.INFO)

        errorLogger.nextLogger = fileLogger
        fileLogger.nextLogger = consoleLogger

        return errorLogger

    def __init__(self):
        self.logger = self.getChainOfLoggers()

        self.logger.logMessage(AbstractLogger.INFO, "Start")
        self.logger.logMessage(AbstractLogger.DEBUG, "debug message")
        self.logger.logMessage(AbstractLogger.ERROR, "error message")
