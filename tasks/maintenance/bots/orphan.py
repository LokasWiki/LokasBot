from core.utils.disambiguation import Disambiguation
import wikitextparser as wtp

from core.utils.helpers import prepare_str


class Orphan:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "يتيمة",
            "Orphan",
            "يتيم",
        ]
        self.parsed = wtp.parse(self.text)

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
        found = False
        for needed_template in self.templates:
            for template in self.parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    found = True
                    break

        if not found:
            new_text = "{{يتيمة|تاريخ ={{نسخ:شهر وسنة}}}}"
            new_text += "\n"
            new_text += self.text

            self.text = new_text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات يتيمة|يتيمة]]"

    def remove_template(self):
        """
           This method removes the {{يتيمة}} template from the page if it exists.
           """
        new_text = self.text
        for needed_template in self.templates:
            for template in self.parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template), "")

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
