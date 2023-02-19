import re

from core.utils.disambiguation import Disambiguation


class Orphan:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary

    def __call__(self):
        disambiguation = Disambiguation(self.page.title(), self.text)
        if disambiguation.check("or"):
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
        This method adds the {{يتيمة}} template to the page if it doesn't already exist.
        """
        template = re.compile(r"{{يتيمة(?:\|[^}]+)?}}")
        if not template.search(self.text):
            text = "{{يتيمة|تاريخ ={{نسخ:شهر وسنة}}}}"
            text += "\n"
            text += self.text

            self.text = text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات يتيمة|يتيمة]]"

    def remove_template(self):
        """
           This method removes the {{يتيمة}} template from the page if it exists.
           """
        template = re.compile(r"{{يتيمة(?:\|[^}]+)?}}")
        new_text = template.sub("", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[:تصنيف:مقالات يتيمة|يتيمة]]"

    def check(self):
        backlinks = self.page.backlinks(namespaces=0, content=False, follow_redirects=True, filter_redirects=False)
        unique_pages = set()
        has_pages = False
        for link in backlinks:
            unique_pages.add(link)
            if len(unique_pages) >= 3:
                has_pages = True
                break
        return has_pages
