import re
import wikitextparser as wtp


class Disambiguation:
    def __init__(self, page_title, page_text):
        self.page_title = str(page_title).lower()
        self.page_text = str(page_text).lower()
        self.list_of_templates = ["توضيح", "Disambig", "صفحة توضيح", "Disambiguation"]

    def check(self, logic="and"):
        if logic.lower() == "and".lower():
            return self.check_text() and self.check_title()
        elif logic.lower() == "or".lower():
            return self.check_text() or self.check_title()

    def check_text(self):
        parsed = wtp.parse(self.page_text)
        template_found = False
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    template_found = True
                    break
        return template_found

    def check_title(self):
        if re.search(r"^\s*\(\s*(توضيح|disambiguation)\s*\)(.*)$", self.page_title) is not None:
            return True
        return False
