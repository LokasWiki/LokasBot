import datetime
import itertools
import pywikibot
from pywikibot import pagegenerators
import time
from bots.unreviewed_article.core import UnreviewedArticle

import pywikibot

import sys

site = pywikibot.Site()

time_before_start = int(sys.argv[1])

start = pywikibot.Timestamp.now() - datetime.timedelta(minutes=time_before_start)
end = pywikibot.Timestamp.now()



gen1 = pagegenerators.RecentChangesPageGenerator(site=site, start=start, end=end, namespaces=[0],reverse=True)
gen2 = pagegenerators.LogeventsPageGenerator(logtype="review",total=3000,site=site,start=start, end=end, namespace=0,reverse=True)

merged_gen = itertools.chain(gen1,gen2)

# To remove duplicate pages from the generator
gen = set(merged_gen)

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
