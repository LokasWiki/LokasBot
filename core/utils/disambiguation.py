import re

import wikitextparser as wtp

from core.utils.helpers import prepare_str


class Disambiguation:
    def __init__(self, page, page_title, page_text):
        self.page = page
        self.page_title = str(page_title).lower()
        self.page_text = str(page_text).lower()
        self.list_of_templates = ["توضيح", "Disambig", "صفحة توضيح", "Disambiguation"]

    def check(self, logic="and"):
        if logic.lower() == "and".lower():
            return (self.check_text() and self.check_title()) or self.have_molecular_formula_set_index_articles()
        elif logic.lower() == "or".lower():
            return (self.check_text() or self.check_title()) or self.have_molecular_formula_set_index_articles()

    def check_text(self):
        parsed = wtp.parse(self.page_text)
        template_found = False
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    template_found = True
                    break
        return template_found

    def have_molecular_formula_set_index_articles(self):
        # Get the categories on the page
        # https://ar.wikipedia.org/w/index.php?title=%D9%86%D9%82%D8%A7%D8%B4_%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AE%D8%AF%D9%85%3A%D9%84%D9%88%D9%82%D8%A7&diff=62065139&oldid=62050903&diffmode=visual
        categories = self.page.categories()
        found = 0
        list_category = [
            'صفحات مجموعات صيغ كيميائية مفهرسة'
        ]
        for cat in categories:
            for needed_cat in list_category:
                if prepare_str(needed_cat) == prepare_str(cat.title(with_ns=False)):
                    found = 1
                    break
        return found

    def check_title(self):
        if re.search(r"\(\s*(توضيح|disambiguation)\s*\)", self.page_title) is not None:
            return True
        return False
