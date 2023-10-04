import pywikibot

from tasks.tahdith_tashkila.src.data_extraction.templates.football_squad import FootballSquad
from tasks.tahdith_tashkila.src.data_translator.classification_context import ClassificationContext
from tasks.tahdith_tashkila.src.data_translator.data_classification.has_ar_post_classification_strategy import \
    HasArPostClassificationStrategy
from tasks.tahdith_tashkila.src.data_translator.data_classification.not_has_ar_post_classification_strategy import \
    NotHasArPostClassificationStrategy
from tasks.tahdith_tashkila.src.data_translator.data_translation.has_ar_post_classification_strategy import \
    HasArPostTranslationHandler
from tasks.tahdith_tashkila.src.data_translator.data_translation.not_has_ar_post_classification_strategy import \
    NotHasArPostTranslationHandler
from tasks.tahdith_tashkila.src.data_translator.translation_chain import TranslationChain
from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger
from tasks.tahdith_tashkila.src.logger.console_logger import ConsoleLogger
from tasks.tahdith_tashkila.src.logger.error_logger import ErrorLogger
from tasks.tahdith_tashkila.src.logger.file_logger import FileLogger
from tasks.tahdith_tashkila.src.template_integration.templates.football_squad import \
    FootballSquad as FootballSquadIntegration


class BotFactory:
    BOT_STATUS_STARTED = 0
    BOT_STATUS_LOADING_PAGE = 1
    BOT_STATUS_DATA_EXTRACTED = 2
    BOT_STATUS_DATA_TRANSLATED = 3
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
        self.data_translator()
        self.template_integrator()
        self.save()
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

        self.ar_text = self.ar_page.text

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

    def data_translator(self):
        # Create classification context and add classification strategies

        classification_context = ClassificationContext()
        classification_context.add_strategy(HasArPostClassificationStrategy())
        classification_context.add_strategy(NotHasArPostClassificationStrategy())

        # Create translation chain and add translation handlers

        translation_chain = TranslationChain()
        translation_chain.add_handler(HasArPostTranslationHandler())
        translation_chain.add_handler(NotHasArPostTranslationHandler())

        updated_data_extractor_list = []

        for item in self.data_extractor_list:
            classification = classification_context.classify(item)
            item.classification = classification
            updated_data_extractor_list.append(item)

        self.data_extractor_list = updated_data_extractor_list
        updated_data_extractor_list = []

        for item in self.data_extractor_list:
            translated_value = translation_chain.translate(item)
            item.translated_value = translated_value
            updated_data_extractor_list.append(item)

        self.data_extractor_list = updated_data_extractor_list
        updated_data_extractor_list = []
        self.status = self.BOT_STATUS_DATA_TRANSLATED

    def template_integrator(self):
        temp_text = self.ar_text
        template_integrator = FootballSquadIntegration(
            text_page=temp_text,
            logger=self.logger
        )
        template_integrator.new_data = self.data_extractor_list
        temp_text = template_integrator.parse()
        self.ar_text = temp_text

    def save(self):
        temp_title_page = str(self.ar_page.title()).replace("قالب:", "مستخدم:LokasBot/تحديث تشكيلة/")
        self.temp_page = pywikibot.Page(self.ar_site, temp_title_page)
        self.temp_page.text = self.ar_text
        self.temp_page.save(
            "بوت:تحديث تشكيلة v0.0.1-beta"
        )
