from abc import ABC, abstractmethod

from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger


class TemplateIntegrator(ABC):

    def __init__(self, text_page: str, logger: AbstractLogger):
        self.text_page = text_page
        self.logger = logger
        self.new_data = None

    @abstractmethod
    def template_name(self):
        pass

    @property
    def new_data(self):
        return self._new_data

    @new_data.setter
    def new_data(self, value):
        self._new_data = value

    @abstractmethod
    def parse(self, page_text: str):
        pass
