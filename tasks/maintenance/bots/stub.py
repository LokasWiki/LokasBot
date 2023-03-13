import logging

import pywikibot
import wikitextparser as wtp
from core.utils.disambiguation import Disambiguation
from core.utils.helpers import prepare_str


class Stub:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.parsed = wtp.parse(self.text)

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
        This method adds the {{بذرة}} template to the page if it doesn't already exist.
        """
        print("add Stub")
        # found = False
        # for needed_template in self.templates:
        #     for template in self.parsed.templates:
        #         if prepare_str(template.name) == prepare_str(needed_template):
        #             found = True
        #             break
        #
        # if not found:
        #     new_text = "{{نهاية مسدودة|تاريخ ={{نسخ:شهر وسنة}}}}"
        #     new_text += "\n"
        #     new_text += self.text
        #
        #     self.text = new_text
        #     self.summary += "، أضاف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def remove_template(self):
        """
           This method removes the {{بذرة}} template from the page if it exists.
           """
        print("remove Stub")
        # new_text = self.text
        # for needed_template in self.templates:
        #     for template in self.parsed.templates:
        #         if prepare_str(template.name) == prepare_str(needed_template):
        #             new_text = str(new_text).replace(str(template), "")
        #
        # if new_text != self.text:
        #     self.text = new_text
        #     self.summary += "، حذف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def check(self):
       status = True

       return  status
