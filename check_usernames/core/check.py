import pywikibot

class CheckPage:
    def __init__(self, site):
        self._title = ""
        self._page = None
        self.site = site
        self._yes = "نعم"
    @property
    def title(self):
        return self._title

    @property
    def yes(self):
        return self._yes

    @title.setter
    def title(self, value):
        self._title = value

    @yes.setter
    def yes(self, value):
        self._yes = value

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

    def run(self):
        text = self.get_page_text()
        if text == self.yes:
            self.clear()
            return True
        return False

    def clear(self):
        self._page.text = ""
        self._page.save("بوت:تم")

