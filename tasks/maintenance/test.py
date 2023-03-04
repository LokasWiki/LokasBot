import pywikibot

from tasks.maintenance.bots.dead_end import DeadEnd

site = pywikibot.Site()

# page_title = "الشاوية (المغرب)"
page_title = "آمنة المنصوري"

page = pywikibot.Page(site, page_title)
rev_id = 60534506 # some revision id

main_summary = "بوت:صيانة V4.8.10"

# obj = DeadEnd(page, page.text, main_summary)
obj = DeadEnd(page, page.getOldVersion(rev_id), main_summary)
text, summary = obj()

print(summary)
print(text)
# page.text = text
# page.save(summary)
