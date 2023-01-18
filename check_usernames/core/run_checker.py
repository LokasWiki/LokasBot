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


class NewUsersChecker:
    def __init__(self):
        self.site = Site()
        self.end_time = datetime.utcnow() - timedelta(days=1)
        self.start_time = datetime.utcnow()
        self.gen = pagegenerators.LogeventsPageGenerator(site=self.site, logtype='newusers',
                                                         start=Timestamp._from_datetime(self.start_time),
                                                         end=Timestamp._from_datetime(self.end_time))
        self.users_list = [page.title() for page in self.gen]

    def check_blocked(self, limit=30):
        x = 0
        for user in self.users_list:
            x += 1
            if x >= limit:
                break

            user_object = User(self.site, user)
            if user_object.is_blocked():
                print(f"{user} is blocked")
            else:
                print(f"{user} is not blocked")


site = Site("ar", "wikipedia")

list_of_offending_words_page = ListOfOffendingWordsPage(site)
list_of_offending_words_page.title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/قائمة الكلمات المخالفة"
list_of_offending_words_page.load_page()

#
# # create an object of NewUsersChecker class
# checker = NewUsersChecker()
# # call the check_blocked method
# checker.check_blocked()
