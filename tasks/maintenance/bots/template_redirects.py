import copy
import json
import os


from core.utils.file import File
from core.utils.helpers import prepare_str
import wikitextparser as wtp


class TemplateRedirects:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        home_path = os.path.expanduser("~")
        file = File(script_dir=home_path)
        file_path = prepare_str('Template_redirects.txt')
        file.set_stub_path(file_path)
        file.get_json_content()
        self.templates = json.loads(file.contents)

    def __call__(self):

        self.fix()
        return self.text, self.summary

    def fix(self):
        text = self.text
        parsed = wtp.parse(self.text)
        # todo: edit this to make it faster
        for need_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(need_template[0]):
                    temp_template = copy.deepcopy(template)
                    temp_template.name = need_template[1]
                    text = str(text).replace(str(template), str(temp_template))
        self.text = text
