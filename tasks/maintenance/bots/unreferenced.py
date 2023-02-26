from core.utils.disambiguation import Disambiguation
import wikitextparser as wtp


class Unreferenced:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "لا مصدر",
            "مصادر",
            "Citations missing",
            "Unreferenced section",
            "Unreferenced",
            "بحاجة إلى مصدر",
            "بدون مصدر",
            "Unreferenced stub",
            "Source",
            "Unreferencedsect",
            "لا مصادر",
            "المصدر",
            "مصدر",
        ]

        self.extra_templates = [
            "مصدر وحيد"
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
        This method adds the {{لا مصدر}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        found = False
        for needed_template in self.templates:
            for template in parsed.templates:
                if template.name.strip().lower() == needed_template.strip().lower():
                    found = True
                    break

        if not found:
            new_text = "{{لا مصدر|تاريخ ={{نسخ:شهر وسنة}}}}"
            new_text += "\n"
            new_text += self.text

            self.text = new_text
            self.summary += "، أضاف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]"

    def remove_template(self):
        """
           This method removes the {{لا مصدر}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if template.name.strip().lower() == needed_template.strip().lower():
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]"

    def have_wikidata_ref(self):
        # Get the categories on the page
        categories = self.page.categories()
        found = False
        for cat in categories:
            print(cat.title(with_ns=False))
            if str('مرجع من ويكي بيانات').strip().lower() == cat.title(with_ns=False).strip().lower():
                found = True
                break

        return found

    def check(self):
        parsed = wtp.parse(self.text)
        tags = parsed.get_tags()
        num_of_ref_tags = 0

        for tag in tags:
            if tag.name.strip().lower() == "ref".strip().lower():
                num_of_ref_tags += 1
                break

        if num_of_ref_tags == 0:
            num_of_ref_tags = self.have_wikidata_ref()

        if num_of_ref_tags == 0:
            return False
        return True
