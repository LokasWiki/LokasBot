import re

import pywikibot

import re


class WikiLinkExtractor:
    def __init__(self, text):
        self.text = text
        self.links = []

    def extract_links(self):
        pattern = re.compile(r'\{\{.*?\}\}', re.IGNORECASE | re.DOTALL)
        templates = re.findall(pattern, self.text)

        for template in templates:
            self.text = self.text.replace(template, "")

        pattern = re.compile(r'\[\[([^:]*?)\]\]', re.IGNORECASE)

        matches = re.findall(pattern, self.text)
        for match in matches:
            if "تصنيف:" not in match.lower() and "Category:" not in match.lower():
                if "|" in match:
                    link = match.split("|")[0]
                else:
                    link = match
                site = pywikibot.Site()
                page_title = link
                tmp_page = pywikibot.Page(site,page_title)
                if tmp_page.exists() and (not tmp_page.isRedirectPage()) and (tmp_page.namespace() == 0):
                    self.links.append(link)
        return list(set(self.links))




class DeadEnd:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary

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
        This method adds the {{نهاية مسدودة}} template to the page if it doesn't already exist.
        """
        template = re.compile(r"{{نهاية مسدودة(?:\|[^}]+)?}}")
        if not template.search(self.text):
            text = "{{نهاية مسدودة|تاريخ ={{نسخ:شهر وسنة}}}}"
            text += "\n"
            text += self.text


            self.text = text
            self.summary += "، أضاف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def remove_template(self):
        """
           This method removes the {{نهاية مسدودة}} template from the page if it exists.
           """
        template = re.compile(r"{{نهاية مسدودة(?:\|[^}]+)?}}")
        new_text = template.sub("", self.text)
        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف  وسم [[:تصنيف:مقالات نهاية مسدودة|نهاية مسدودة]]"

    def check(self):
        extractor = WikiLinkExtractor(self.text)
        links = extractor.extract_links()
        num_of_links = len(links)
        if num_of_links == 0:
            return False
        return True
