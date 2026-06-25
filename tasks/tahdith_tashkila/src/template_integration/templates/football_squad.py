import copy
from abc import ABC

import wikitextparser as wtp

from core.utils.helpers import prepare_str
from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger
from tasks.tahdith_tashkila.src.template_integration.template_integrator import TemplateIntegrator


class FootballSquad(TemplateIntegrator, ABC):

    def __init__(self, text_page: str, logger: AbstractLogger):
        super().__init__(text_page=text_page, logger=logger)

    def template_name(self):
        return "شريط تصفح تشكيلة فريق كرة قدم"

    def parse(self):
        parser = wtp.parse(self.text_page)
        for template in parser.templates:
            temp_template = copy.deepcopy(template)
            if prepare_str(temp_template.name) == prepare_str(self.template_name()):
                for param in temp_template.arguments:
                    if prepare_str(param.name) == prepare_str("القائمة"):
                        param.value = self.get_new_list()
            self.text_page = str(self.text_page).replace(str(template), str(temp_template))
        return self.text_page

    def get_new_list(self):
        temp_text = ""
        for model in self.new_data:
            temp_text += model.translated_value
            temp_text += "{{فاصل}}"
            temp_text += "\n"
        return temp_text
