import re

import pywikibot
from core.utils.disambiguation import Disambiguation
import wikitextparser as wtp


class Protection:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.templates = [
            "محمية",
            "Protected",
            "حماية خاصة",
            "حماية نزاع",
            "Pp-semi-template",
            "Pp-semi-vandalism",
            "Pp-dispute",
            "قفل",
            "Pp-semi-protected",
            "Pp-move-indef",
            "Pp-protected",
            "حماية كلية",
            "حماية حرب",
            "حماية جزئية",
            "Pp-semi",
            "حماية كاملة",
            "حماية",
            "صفحة محمية",
            "Semi-protection",
            "Pp-semi-indef",
            "شبه محمي",
            "حماية تخريب"
        ]

        self.summary = summary

    def __call__(self):

        if self.check():
            self.add_template()

        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{بذرة غير مصنفة}} template to the page if it doesn't already exist.
        """
        pass
        # template = re.compile(r"{{بذرة غير مصنفة(?:\|[^}]+)?}}")
        # if not template.search(self.text):
        #     text = self.text
        #     text += "\n"
        #     text += "{{بذرة غير مصنفة|تاريخ ={{نسخ:شهر وسنة}}}}"
        #
        #     self.text = text
        #     self.summary += "، أضاف  وسم [[:تصنيف:مقالات غير مصنفة|غير مصنفة]]"

    def remove_template(self):
        """
           This method removes the {{محمية}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if template.name.strip().lower() == needed_template.strip().lower():
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، إزالة قالب الحماية"

    def check(self):
        protection = self.page.protection()
        has_protection = False

        # The dictionary is not empty that mean page have protection
        if bool(protection):
            has_protection = True
            print("The dictionary is not empty")

        return has_protection
