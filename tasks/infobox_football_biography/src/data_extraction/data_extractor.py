from abc import abstractmethod, ABC

import wikitextparser as wtp

from core.utils.helpers import prepare_str
from tasks.infobox_football_biography.src.logger.abstract_logger import AbstractLogger


class DataExtractor(ABC):
    def __init__(self, text_page: str, logger: AbstractLogger):
        self.text_page = text_page
        self.logger = logger
        self.list = []

    @abstractmethod
    def template_name(self) -> str:
        pass

    @abstractmethod
    def parameters_list(self) -> list:
        pass

    def check(self) -> bool:
        return len(self.list) > 0

    def parse(self):
        self.logger.logMessage(AbstractLogger.INFO, "start extract data")
        parsed = wtp.parse(self.text_page)
        self.logger.logMessage(AbstractLogger.INFO, "end extract data")
        self.logger.logMessage(AbstractLogger.INFO, "start extract template")
        templates = parsed.templates
        if not len(templates):
            self.logger.logMessage(AbstractLogger.WARNING, "no template found in page")
            return
        if self.template_name() is None:
            self.logger.logMessage(AbstractLogger.ERROR, "no template name set in class you are using")
            return
        if self.parameters_list() is None or len(self.parameters_list()) == 0:
            self.logger.logMessage(AbstractLogger.ERROR, "no parameters set in class you are using")
            return
        for template in templates:
            if prepare_str(template.name) == prepare_str(self.template_name()):
                self.logger.logMessage(AbstractLogger.INFO, "start extract parameters")
                for parameter in self.parameters_list():
                    for param in template.arguments:
                        if prepare_str(param.name) == prepare_str(parameter):
                            self.logger.logMessage(AbstractLogger.INFO, f"{param.name}: {param.value}")
                            self.list.append({
                                "name": param.name,
                                "value": param.value
                            })
                break
