import re

import pywikibot
import requests


class UnreviewedArticle:
    def __init__(self, site):
        self._title = ""
        self._page = None
        self.site = site

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def page(self):
        return self._page

    def load_page(self):
        self._page = pywikibot.Page(self.site, self.title)

    def get_page_text(self):
        if self._page is None:
            self.load_page()
        text = self._page.text
        return text

    def add_template(self):
        text = self.page.text
        template = re.compile(r"{{مقالة غير مراجعة(?:\|[^}]+)?}}")
        if not template.search(text):
            newText = "{{مقالة غير مراجعة|تاريخ = {{safesubst:#وقت:F Y}}}}"
            newText += "\n"
            newText += text
            self._page.text = newText
            self._page.save("بوت:صيانة V1.0، أضاف وسم مقالة غير مراجعة")

    def remove_template(self):
        text = self.page.text
        template = re.compile(r"{{مقالة غير مراجعة(?:\|[^}]+)?}}")
        new_text = template.sub("", text)
        if new_text != text:
            self.page.text = new_text
            self._page.save("بوت:صيانة V1.0، حذف وسم مقالة غير مراجعة")

    def check(self):
        params = {
            "action": "query",
            "format": "json",
            "prop": "info|flagged",
            "titles": self.page.title(),
            "formatversion": 2
        }

        request = pywikibot.data.api.Request(site=self.page.site, **params)
        data = request.submit()
        pages = data["query"]["pages"]
        for page in pages:
            if "flagged" in page:
                if page["flagged"]:
                    return True
        return False
