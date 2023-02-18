import time

import pywikibot
from tasks.webcite.modules.parsed import Parsed

site = pywikibot.Site()


titles = [
   "ليلى حيدري"
]


for page_name in titles:
    page = pywikibot.Page(site, page_name)
    if page.exists():
        summary = ""
        print(page.title())
        bot = Parsed(page.text, summary)
        new_text, new_summary = bot()
        if new_text != page.text:
            print("start save page")
            page.text = new_text
            page.save(new_summary)
        time.sleep(30)
