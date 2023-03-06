import pywikibot
from core.utils.disambiguation import Disambiguation
from core.utils.helpers import prepare_str
import wikitextparser as wtp


class UnderLinked:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "وصلات قليلة",
            "Wikify",
            "Wiki",
            "Underlinked",
            "ويكي"
        ]

    def __call__(self):
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
        This method adds the {{وصلات قليلة}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        found = False
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    found = True
                    break

        if not found:
            new_text = "{{وصلات قليلة|تاريخ ={{نسخ:شهر وسنة}}}}"
            new_text += "\n"
            new_text += self.text

            self.text = new_text
            self.summary += "، أضاف  وسم [[ويكيبيديا:وصلات قليلة|وصلات قليلة]]"

    def remove_template(self):
        """
           This method removes the {{وصلات قليلة}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[ويكيبيديا:وصلات قليلة|وصلات قليلة]]"

    def check(self):
        # todo:split this code
        links_list = []
        parsed = wtp.parse(self.text)
        links = parsed.wikilinks
        for link in links:
            temp_page = pywikibot.Page(self.page.site, link.title)
            if temp_page.exists() and temp_page.namespace() == 0:
                if temp_page.isRedirectPage():
                    temp_page_redirect = temp_page.getRedirectTarget()
                    if temp_page_redirect.exists() and temp_page_redirect.namespace() == 0:
                        links_list.append(prepare_str(link.title))
                        if len(list(set(links_list))) >= 4:
                            break
                else:
                    links_list.append(prepare_str(link.title))
                    if len(list(set(links_list))) >= 4:
                        break
        status = False
        if 1 <= len(list(set(links_list))) < 3:
            status = True

        return status
