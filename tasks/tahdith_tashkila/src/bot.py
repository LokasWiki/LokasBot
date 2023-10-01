import pywikibot

from tasks.tahdith_tashkila.src.data_extraction.templates.football_squad import FootballSquad
from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger
from tasks.tahdith_tashkila.src.logger.console_logger import ConsoleLogger
from tasks.tahdith_tashkila.src.logger.error_logger import ErrorLogger
from tasks.tahdith_tashkila.src.logger.file_logger import FileLogger


class BotFactory:
    BOT_STATUS_STARTED = 0
    BOT_STATUS_LOADING_PAGE = 1
    BOT_STATUS_DATA_EXTRACTED = 2

    def getChainOfLoggers(self) -> AbstractLogger:
        errorLogger = ErrorLogger(AbstractLogger.ERROR)
        fileLogger = FileLogger(AbstractLogger.DEBUG)
        consoleLogger = ConsoleLogger(AbstractLogger.INFO)

        errorLogger.nextLogger = fileLogger
        fileLogger.nextLogger = consoleLogger

        return errorLogger

    def run(self, page_title: str):
        self.logger.logMessage(AbstractLogger.INFO, "Bot started")
        self.load_page(page_title=page_title)
        self.data_extractor()
        self.logger.logMessage(AbstractLogger.INFO, "Bot finished")

    def __init__(self):
        self.logger = self.getChainOfLoggers()
        # ar page
        self.ar_site = pywikibot.Site("ar", "wikipedia")
        self.ar_page = None
        self.ar_text = None
        # en page
        self.en_site = pywikibot.Site("en", "wikipedia")
        self.en_page = None
        self.en_text = None
        self.status = self.BOT_STATUS_STARTED

        self.data_extractor_list = []

    def load_page(self, page_title: str):
        self.logger.logMessage(AbstractLogger.INFO, "start loading page")
        self.ar_page = pywikibot.Page(self.ar_site, page_title)
        if not self.ar_page.exists():
            self.logger.logMessage(AbstractLogger.ERROR, "page does not exist")
            return
        self.logger.logMessage(AbstractLogger.INFO, "page exists")
        en_title = None
        for item in self.ar_page.langlinks():
            if str(item).startswith("[[en:"):
                en_title = item.title
                break
        if en_title is None:
            self.logger.logMessage(AbstractLogger.ERROR, "en page not found")
        en_title_with_template = "template:" + en_title
        self.logger.logMessage(AbstractLogger.INFO, "start geting en page")
        self.en_page = pywikibot.Page(self.en_site, en_title_with_template)

        if not self.en_page.exists():
            self.logger.logMessage(AbstractLogger.ERROR, "page does not exist")
            return

        self.logger.logMessage(AbstractLogger.INFO, "en page exists")

        self.en_text = self.en_page.text

        self.ar_text = self.ar_text

        self.logger.logMessage(AbstractLogger.INFO, "end fill page")

        self.status = self.BOT_STATUS_LOADING_PAGE

    def data_extractor(self):
        self.logger.logMessage(AbstractLogger.INFO, "start extract template")
        extractor = FootballSquad(
            text_page=self.en_text,
            logger=self.logger
        )
        extractor.parse()
        if not extractor.check():
            self.logger.logMessage(AbstractLogger.ERROR, "cannot found data in this template")

        self.data_extractor_list = extractor.list
        self.status = self.BOT_STATUS_DATA_EXTRACTED
