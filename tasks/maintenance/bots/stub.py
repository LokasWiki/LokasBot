import logging
import re

import pywikibot
import wikitextparser as wtp
from core.utils.disambiguation import Disambiguation
from core.utils.helpers import prepare_str, check_status


class Stub:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.parsed = wtp.parse(self.text)
        self.count_words = 0

    def __call__(self):
        if check_status("مستخدم:LokasBot/إيقاف بوت البذرة"):
            disambiguation = Disambiguation(self.page.title(), self.text)
            if disambiguation.check("or"):
                return self.text, self.summary

            if self.check():
                self.add_template()
            else:
                self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{بذرة}} template to the page if it doesn't already exist.
        """
        print("add Stub")
        text = self.text
        found = False
        for template in self.parsed.templates:
            if prepare_str(template.name).startswith("بذرة"):
                if not (prepare_str(template.name) == prepare_str("بذرة غير مصنفة")):
                    found = True
                    break

        if not found:
            template_name = "{{بذرة}}"
            added = False
            if not added:
                for template in self.parsed.templates:
                    if prepare_str(template.name) == prepare_str("شريط بوابات"):
                        text = self.text.replace(str(template), str(template) + '\n' + template_name, 1)
                        added = True
                        break

            if not added:
                for template in self.parsed.templates:
                    if prepare_str(template.name) == prepare_str("مقالات بحاجة لشريط بوابات"):
                        text = self.text.replace(str(template), str(template) + '\n' + template_name, 1)
                        added = True
                        break

            if not added:
                category_template = '[[تصنيف:'
                if category_template in self.text:
                    text = self.text.replace(category_template, template_name + '\n' + category_template, 1)
                else:
                    text = self.text + '\n' + template_name

            self.text = text
            self.summary += "،  أضاف [[ويكيبيديا:بذرة|بذرة]] (" + str(self.count_words) + " كلمة)"

    def remove_template(self):
        """
           This method removes the {{بذرة}} template from the page if it exists.
           """
        new_text = self.text

        for template in self.parsed.templates:
            if prepare_str(template.name).startswith("بذرة"):
                if not (prepare_str(template.name) == prepare_str("بذرة غير مصنفة")):
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، أزال [[ويكيبيديا:بذرة|بذرة]] (" + str(self.count_words) + " كلمة)"

    def check(self):
        status = True

        tem_text = self.page.text

        parsed = wtp.parse(tem_text)

        # remove cat links
        for link in parsed.wikilinks:
            if ":" in link.title:
                tem_text = tem_text.replace(str(link), "")
        parsed = wtp.parse(tem_text)
        # remove tables
        # remove template
        # remove html tag include ref tags
        # remove all comments
        # remove all external links
        tem_text = parsed.plain_text(
            replace_wikilinks=False,
            replace_bolds_and_italics=False
        )
        parsed = wtp.parse(tem_text)
        # replace all wikilinks to be like  [from|some text ] to from
        for wikilink in parsed.wikilinks:
            tem_text = tem_text.replace(str(wikilink), str(wikilink.title))

        # remove tables like this "{| |}"
        tem_text = re.sub(r"{|\|[.|\w|\W]*?\|}", "", tem_text)

        # remove numbers in string"
        tem_text = re.sub(r"\d+", "", tem_text)

        # get counts of words
        result = len(re.findall(r'\w+', tem_text))
        self.count_words = result
        if result >= 500:
            # start remove template
            status = False

        return status
