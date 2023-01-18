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

    def check_blocked(self, limit=30):
        x = 0
        for user in self.users_list:
            x += 1
            if x >= limit:
                break
            user_object = User(self.site, user)
            if not user_object.is_blocked():
               self.list.append(user)


site = Site("ar", "wikipedia")
list_of_offending_words_page_title  = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/قائمة الكلمات المخالفة"
list_of_offending_words_page = ListOfOffendingWordsPage(site)
list_of_offending_words_page.title = list_of_offending_words_page_title
list_of_offending_words_page.load_page()


scanner = RequestsScanner()

scanner.pattern = r'\* "(?P<word>[^"]*)"'
scanner.scan(list_of_offending_words_page.get_page_text())
if scanner.have_requests:
    wordList = scanner.requests
    checker = NewUsersChecker()
    checker.check_blocked()
    usersList = checker.list
    result = [match['word'] for match in wordList]
    # phrases_regex = '|'.join(result)
    # print(phrases_regex)
    for user in usersList:
        for phrases_regex in result:
            matches = re.findall(phrases_regex, str(user))
            if matches:
                print(user,matches)
                break
else:
    print(f"there is no words in page {list_of_offending_words_page_title}")

#
# # create an object of NewUsersChecker class
# checker = NewUsersChecker()
# # call the check_blocked method
# checker.check_blocked()
