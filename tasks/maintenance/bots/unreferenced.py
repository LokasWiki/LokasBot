from core.utils.disambiguation import Disambiguation
import wikitextparser as wtp

from core.utils.helpers import prepare_str


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
        if disambiguation.check("or") or self.check_skip():
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
                if prepare_str(template.name) == prepare_str(needed_template):
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
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]"

    def have_wikidata_ref(self):
        # Get the categories on the page

        categories = self.page.categories()
        found = 0
        list_category = [
            'مرجع من ويكي بيانات', 'صفحات بها مراجع ويكي بيانات'
        ]
        for cat in categories:
            for needed_cat in list_category:
                if prepare_str(needed_cat) == prepare_str(cat.title(with_ns=False)):
                    found = 1
                    break
        return found

    def check_skip(self):
        # todo:add test to this
        # https://ar.wikipedia.org/w/index.php?title=%D9%86%D9%82%D8%A7%D8%B4_%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AE%D8%AF%D9%85:%D9%84%D9%88%D9%82%D8%A7&oldid=61348322#%D8%AE%D8%B7%D8%A3_%D9%84%D9%84%D8%A8%D9%88%D8%AA
        categories = self.page.categories()
        skip = 0
        list_category = [
            'بوابة تقويم/مقالات متعلقة',
            'بوابة سنوات/مقالات متعلقة',
        ]
        for cat in categories:
            for needed_cat in list_category:
                if prepare_str(needed_cat) == prepare_str(cat.title(with_ns=False)):
                    skip = 1
                    break
        return skip

    def check(self):
        parsed = wtp.parse(self.text)
        tags = parsed.get_tags()
        num_of_ref_tags = 0
        # check tags
        for tag in tags:
            if prepare_str(tag.name) == prepare_str("ref"):
                num_of_ref_tags += 1
                break
        #   check template
        if num_of_ref_tags == 0:
            templates = parsed.templates
            list_of_cites_template = ['sfn']
            for needed_template in list_of_cites_template:
                for template in templates:
                    if prepare_str(needed_template) == prepare_str(template.name):
                        num_of_ref_tags += 1
                        break
        # chcek wikdata
        if num_of_ref_tags == 0:
            num_of_ref_tags = self.have_wikidata_ref()

        if num_of_ref_tags == 0:
            return False
        return True
