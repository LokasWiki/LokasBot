import re

import pywikibot
from core.utils.helpers import prepare_str


class RequestsScanner:
    def __init__(self):
        self._pattern = None
        self._requests = []
        self._have_requests = False

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = re.compile(value)

    @property
    def requests(self):
        return self._requests

    @property
    def have_requests(self):
        return self._have_requests

    def scan(self, text):
        matches = self._pattern.finditer(text)
        self._requests = []
        for match in matches:
            request = match.groupdict()
            self._requests.append(request)
        if self._requests:
            self._have_requests = True
        else:
            self._have_requests = False


class RequestsPage:
    def __init__(self, site):
        self._title = ""
        self._header_text = ""
        self._page = None
        self._lasteditUser = None
        self.site = site

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def header_text(self):
        return self._header_text

    @header_text.setter
    def header_text(self, value):
        self._header_text = value

    @property
    def page(self):
        return self._page

    @property
    def lasteditUser(self):
        return self._lasteditUser

    def load_page(self):
        self._page = pywikibot.Page(self.site, self.title)
        self._lasteditUser = self._page.lastNonBotUser()

    def check_user_edits(self, number=3000):
        user = pywikibot.User(self.site, self.lasteditUser)
        return user.editCount() >= number
        # return True

    def check_user_groups(self, group):
        user = pywikibot.User(self.site, self.lasteditUser)
        found = False
        for g in user.groups():
            if prepare_str(g) == prepare_str(group):
                found = True
                break
        return found

    def get_page_text(self):
        if self._page is None:
            self.load_page()
        text = self._page.text
        text = text.replace(self.header_text, "", 1)
        return text

    def move_to_talk_page(self):
        talk_page = self._page.toggleTalkPage()
        tem_page_text = self._page.text

        text = talk_page.text
        text += "\n\n== طلب جديد عبر البوت من المستخدم " + self.lasteditUser + "==\n\n"
        text += "{{ر|Dr-Taher|" + self.lasteditUser + "}}"
        text += str(self._page.text).replace(self._header_text, "")
        text += "\n~~~~"
        talk_page.text = text
        self._page.text = self._header_text + "\n\n"

        if tem_page_text.strip().lower() != self._header_text.strip().lower():
            talk_page.save(summary=" طلب جديد عبر البوت من المستخدم " + str(self.lasteditUser), minor=False)
            self._page.save(summary=" نقل طلب جديد غير مصرح به من المستخدم إلي الأرشيف " + str(self.lasteditUser),
                            minor=False)

    def start_request(self):
        self._page.text = self._header_text + "\n\n"
        self._page.save("جاري العمل")


class PageProcessor:
    def __init__(self, site, requests_query):
        self.site = site
        self.requests_query = requests_query

    def process_pages(self):
        request = self.requests_query.pop_request()
        if request:
            namespace, page_name, target_page, _ = request
            pages = []
            if namespace == "تصنيف":
                category = pywikibot.Category(self.site, f"تصنيف:{page_name}")
                pages = category.articles()
            elif namespace == "قالب":
                template = pywikibot.Page(self.site, f"قالب:{page_name}")
                pages = template.usingPages()
            return pages
        return None