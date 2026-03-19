from abc import ABC

import wikitextparser as wtp

from core.utils.helpers import prepare_str
from tasks.tahdith_tashkila.src.data_extraction.data_extractor import DataExtractor
from tasks.tahdith_tashkila.src.logger.abstract_logger import AbstractLogger
from tasks.tahdith_tashkila.src.models.player import Player


class FootballSquad(DataExtractor, ABC):
    def __init__(self, text_page: str, logger: AbstractLogger):
        super().__init__(text_page=text_page, logger=logger)

    def template_name(self) -> str:
        return "Football squad"

    def parameters_list(self) -> list:
        return [
            "no##",
            "manager##",
            "manager_type##",
            "list"
        ]

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

                have_list_argument = False

                for argument in template.arguments:
                    if prepare_str(argument.name) == prepare_str('list'):
                        have_list_argument = True
                        break

                if have_list_argument:
                    for sub_template in parsed.templates:
                        if prepare_str(sub_template.name) == prepare_str("football squad2 player"):
                            temp_dic = {}
                            for temp_arg in sub_template.arguments:
                                temp_dic[temp_arg.name] = temp_arg.value

                            player = Player()
                            player.title = None
                            player.name = temp_dic["name"] if 'name' in temp_dic else None
                            player.number = temp_dic["no"] if 'no' in temp_dic else None
                            player.is_manager = False
                            self.list.append(player)

                        if prepare_str(sub_template.name) == prepare_str("football squad manager"):
                            temp_dic = {}
                            for temp_arg in sub_template.arguments:
                                temp_dic[temp_arg.name] = temp_arg.value
                            player = Player()
                            player.title = temp_dic['title'] if 'title' in temp_dic else None
                            player.name = temp_dic["name"] if 'name' in temp_dic else None
                            player.number = None
                            player.is_manager = True
                            self.list.append(player)

                # if not have_list_argument:
                #     for param in template.arguments:
                #         for parameter in self.parameters_list():
                #             tem_parameter = str(parameter).replace("#", "")
                #             if prepare_str(param.name).startswith(tem_parameter):
                #                 self.logger.logMessage(AbstractLogger.INFO, f"{param.name}: {param.value}")
                #                 self.list.append({
                #                     "name": param.name,
                #                     "value": param.value
                #                 })
