import pywikibot
from core.utils.disambiguation import Disambiguation
import wikitextparser as wtp

from core.utils.helpers import prepare_str


class HasCategories:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "بذرة غير مصنفة"
        ]

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
        This method adds the {{بذرة غير مصنفة}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        found = False
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    found = True
                    break

        if not found:
            new_text = self.text
            new_text += "\n"
            new_text += "{{بذرة غير مصنفة|تاريخ ={{نسخ:شهر وسنة}}}}"

            self.text = new_text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات غير مصنفة|غير مصنفة]]"

    def remove_template(self):
        """
           This method removes the {{بذرة غير مصنفة}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[:تصنيف:مقالات غير مصنفة|غير مصنفة]]"

    def check(self):
        categories = self.page.categories()
        has_category = False
        seen_categories = set()
        for category in categories:
            tem = pywikibot.Category(self.page.site, category.title())
            # todo: fix this logic to check Redirect cat
            if not tem.isHiddenCategory() and tem.exists() and (not tem.isRedirectPage()):
                if len(seen_categories) == 1:
                    break
                if category.title() not in seen_categories:
                    seen_categories.add(category.title())
                    has_category = True
        return has_category
