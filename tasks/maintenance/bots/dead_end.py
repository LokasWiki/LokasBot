import re

import pywikibot

from core import WikiLinkExtractor
class DeadEnd:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary

    def __call__(self):
        if "(توضيح)" in self.page.title() or "{{توضيح" in self.text:
            return self.text, self.summary
        """
            true mean has category -> remove
            false mean not have category -> add
        :return:
        """
        if not self.check():
            self.add_template()
        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{نهاية مسدودة}} template to the page if it doesn't already exist.
        """
        template = re.compile(r"{{نهاية مسدودة(?:\|[^}]+)?}}")
        if not template.search(self.text):
            text = self.text
            text += "\n"
            text += "{{نهاية مسدودة|تاريخ ={{نسخ:شهر وسنة}}}}"

            self.text = text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def remove_template(self):
        """
           This method removes the {{نهاية مسدودة}} template from the page if it exists.
           """
        template = re.compile(r"{{نهاية مسدودة(?:\|[^}]+)?}}")
        new_text = template.sub("", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def check(self):
        extractor = WikiLinkExtractor(self.text)
        links = extractor.extract_links()
        num_of_links = len(links)
        if num_of_links == 0:
            return False
        return True
