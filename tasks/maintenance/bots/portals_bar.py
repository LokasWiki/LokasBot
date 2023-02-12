import re
import wikitextparser as wtp

from core.utils.disambiguation import Disambiguation


class PortalsBar:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary

    def __call__(self):
        disambiguation = Disambiguation(self.page.title(),self.text)
        if disambiguation.check("or"):
            return self.text, self.summary

        if not self.check():
            self.add_template()
        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{مقالات بحاجة لشريط بوابات}} template to the page if it doesn't already exist.
        """
        template = re.compile(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*")
        if not template.search(self.text):
            template_name = "{{مقالات بحاجة لشريط بوابات}}"
            category_template = '[[تصنيف:'
            if category_template in self.text:
                text = self.text.replace(category_template, template_name + '\n' + category_template, 1)
            else:
                text = self.text + '\n' + template_name
            self.text = text

            # todo:remove empty Portals Bar bar
            self.summary += "، أضاف وسم مقالات بحاجة لشريط بوابات"

    def remove_template(self):
        """
           This method removes the {{مقالات بحاجة لشريط بوابات}} template from the page if it exists.
           """
        template = re.compile(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*")
        new_text = template.sub("\n", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف وسم مقالات بحاجة لشريط بوابات"

    def check(self):
        pattern = r"{{\s*شريط\s+(ال)?\s*بوابات\s*\|\s*[\w\W\s]+\s*}}"
        result = re.search(pattern, self.text)
        if result:
            return True
        return False
