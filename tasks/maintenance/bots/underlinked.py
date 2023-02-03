import re

import pywikibot
from core import WikiLinkExtractor

class Underlinked:
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
        This method adds the {{وصلات قليلة}} template to the page if it doesn't already exist.
        """
        template = re.compile(r"{{وصلات قليلة(?:\|[^}]+)?}}")
        if not template.search(self.text):
            text = self.text
            text += "\n"
            text += "{{وصلات قليلة|تاريخ ={{نسخ:شهر وسنة}}}}"

            self.text = text
            self.summary += "، أضاف  وسم [[ويكيبيديا:وصلات قليلة|وصلات قليلة]]"

    def remove_template(self):
        """
           This method removes the {{وصلات قليلة}} template from the page if it exists.
           """
        template = re.compile(r"{{وصلات قليلة(?:\|[^}]+)?}}")
        new_text = template.sub("", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[ويكيبيديا:وصلات قليلة|وصلات قليلة]]"

    def check(self):
        extractor = WikiLinkExtractor(self.text)
        links = extractor.extract_links()
        num_of_links = len(links)
        if 1 <= num_of_links < 3:
            return False
        return True
