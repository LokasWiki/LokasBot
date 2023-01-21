import datetime

import pywikibot
from pywikibot import pagegenerators
import time
from bots.unreviewed_article.core import UnreviewedArticle

import pywikibot

site = pywikibot.Site()

start = pywikibot.Timestamp.now() - datetime.timedelta(hours=6)
end = pywikibot.Timestamp.now()


gen = pagegenerators.RecentChangesPageGenerator(site=site, start=start, end=end, namespaces=[0],reverse=True)

# To remove duplicate pages from the generator
gen = set(gen)

# To remove deleted pages from the generator,
gen = filter(lambda page: page.exists(), gen)

for entry in gen:

    page1 = pywikibot.Page(site, entry.title())
    if not page1.isRedirectPage():
        time.sleep(2)
        print(entry.title())
        try:
            title = entry.title()
            page = UnreviewedArticle(site)
            page.title = title
            page.load_page()
            if not page.check():
                page.add_template()
            else:
                page.remove_template()
        except Exception as e:
            print(f"An error occurred while processing {entry.title()}: {e}")
