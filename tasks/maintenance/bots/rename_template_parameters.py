import copy
import json
import logging
import os

from core.utils.file import File
from core.utils.helpers import prepare_str
import wikitextparser as wtp


def replace_to(searched_list, arg, template):
    my_arg = None
    for need_arg in searched_list:
        if template.has_arg(need_arg.strip().lower()):
            tem_arg = copy.deepcopy(template.get_arg(need_arg.strip().lower()))
            if len(tem_arg.value) >= 10:
                template.del_arg(need_arg.strip().lower())
                my_arg = tem_arg

    if my_arg is not None:
        template.set_arg(arg.strip().lower(), my_arg.value.strip())
    return template


class RenameTemplateParameters:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        home_path = os.path.expanduser("~")
        file = File(script_dir=home_path)
        file_path = prepare_str('rename_template_parameters.txt')
        file.set_stub_path(file_path)
        file.get_json_content()
        self.templates = json.loads(file.contents)

    def __call__(self):

        temp_text = self.text
        self.fix()
        if temp_text != self.text:
            self.summary += "، تعريب"
        return self.text, self.summary

    def fix(self):
        text = self.text
        parsed = wtp.parse(self.text)
        # todo: edit this to make it faster
        for need_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(need_template[0]):
                    for saved_new_parameter in need_template[1]:
                        try:
                            from_str = saved_new_parameter[0]
                            to_str = saved_new_parameter[1]
                            text = str(text).replace(str(template), str(replace_to([from_str], to_str, template)))
                        except Exception as e:
                            logging.exception(e)

        self.text = text
