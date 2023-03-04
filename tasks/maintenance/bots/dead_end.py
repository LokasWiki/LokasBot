import pywikibot
import wikitextparser as wtp
import re
from core.utils.disambiguation import Disambiguation

class DeadEnd:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "نهاية مسدودة",
            "Deadend",
            "Dead end",
            "Internallinks"
        ]

    def __call__(self):
        disambiguation = Disambiguation(self.page.title(), self.text)
        if disambiguation.check("or"):
            return self.text, self.summary

        if not self.check():
            self.add_template()
        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{نهاية مسدودة}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        found = False
        for needed_template in self.templates:
            for template in parsed.templates:
                if template.name.strip().lower() == needed_template.strip().lower():
                    found = True
                    break

        if not found:
            new_text = "{{نهاية مسدودة|تاريخ ={{نسخ:شهر وسنة}}}}"
            new_text += "\n"
            new_text += self.text

            self.text = new_text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def remove_template(self):
        """
           This method removes the {{نهاية مسدودة}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if template.name.strip().lower() == needed_template.strip().lower():
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def check(self):
        number_of_link = 0
        parsed = wtp.parse(self.text)
        links = parsed.wikilinks
        for link in links:
            temp_page = pywikibot.Page(self.page.site,link.title)
            if temp_page.exists() and temp_page.namespace() == 0:
                if temp_page.isRedirectPage():
                    temp_page_redirect = temp_page.getRedirectTarget()
                    if temp_page_redirect.exists() and temp_page_redirect.namespace() == 0:
                        number_of_link = 1
                        break
                else:
                    number_of_link = 1
                    break

        return bool(number_of_link)
