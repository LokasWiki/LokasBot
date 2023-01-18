import re
from datetime import timedelta, datetime

import pywikibot
from pywikibot import Site, pagegenerators, Timestamp, User


class ListOfOffendingWordsPage:
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


class NewUsersChecker:
    def __init__(self):
        self.site = Site()
        self.end_time = datetime.utcnow() - timedelta(days=1)
        self.start_time = datetime.utcnow()
        self.gen = pagegenerators.LogeventsPageGenerator(site=self.site, logtype='newusers',
                                                         start=Timestamp._from_datetime(self.start_time),
                                                         end=Timestamp._from_datetime(self.end_time))
        self.users_list = [page.title() for page in self.gen]
        self.list = []

    def check_blocked(self):
        for user in self.users_list:
            user_object = User(self.site, user)
            if not user_object.is_blocked():
                self.list.append(user)


class NewUsersCheckerPage:
    def init(self):
        self.site = Site("ar", "wikipedia")
        self.list_of_offending_words_page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/قائمة الكلمات المخالفة"
        self.list_of_offending_words_page = ListOfOffendingWordsPage(self.site)
        self.list_of_offending_words_page.title = self.list_of_offending_words_page_title
        self.list_of_offending_words_page.load_page()

    def check_blocked(self):
        scanner = RequestsScanner()
        scanner.pattern = r'\* "(?P<word>[^"]*)"'
        scanner.scan(self.list_of_offending_words_page.get_page_text())
        if scanner.have_requests:
            wordList = scanner.requests
            checker = NewUsersChecker()
            checker.check_blocked()
            usersList = checker.list
            result = [match['word'] for match in wordList]
            for user in usersList:
                match_found = False
                for phrases_regex in result:
                    if re.search(re.escape(phrases_regex), str(user)):
                        match_found = True
                        print(phrases_regex)
                        break
                if match_found:
                    print(user)
        else:
            print(f"there is no words in page {self.list_of_offending_words_page_title}")


new_users_checker = NewUsersCheckerPage()
new_users_checker.check_blocked()