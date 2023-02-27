import pywikibot


class Check:
    def __init__(self, site, page_title):
        self.page_title = page_title
        self.site = site
        self.text = None
        self.page = None

    def load(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        if self.page.exists():
            self.text = self.page.text

    def check(self):
        if self.text is not None:
            if self.text.strip().lower() == str("نعم").strip().lower():
                return True
        return False

    def reload(self):
        self.page.text = "لا"
        self.page.save("بوت:تم")


site = pywikibot.Site()
check_page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت"
check_page = Check(site=site, page_title=check_page_title)
check_page.load()
if check_page.check():
    check_page.reload()
#     todo:start send alert
