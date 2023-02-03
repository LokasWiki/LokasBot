import re

import pywikibot


class Unreferenced:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = ["لا مصدر", "مصدر"]

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
        This method adds the {{لا مصدر}} template to the page if it doesn't already exist.
        """
        pattern = r"{{(" + "|".join(self.templates) + r")(.*?)}}"

        template = re.compile(pattern)
        if not template.search(self.text):
            text = "{{لا مصدر|تاريخ ={{نسخ:شهر وسنة}}}}"
            text += "\n"
            text += self.text


            self.text = text
            self.summary += "، أضاف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]"

    def remove_template(self):
        """
           This method removes the {{لا مصدر}} template from the page if it exists.
           """
        pattern = r"{{(" + "|".join(self.templates) + r")(.*?)}}"
        template = re.compile(pattern)
        new_text = template.sub("", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]"

    def check(self):
        pattern = r"<ref.*?>([.\w\W]*?)<\/ref>"
        ref_tags = re.findall(pattern, self.text)
        num_of_ref_tags = len(ref_tags)
        if num_of_ref_tags == 0:
            return False
        return True
