from datetime import timedelta, datetime
from pywikibot import Site, pagegenerators, Timestamp, User


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


# create an object of NewUsersChecker class
checker = NewUsersChecker()
# call the check_blocked method
checker.check_blocked()
