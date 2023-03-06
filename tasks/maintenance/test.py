import pywikibot

from tasks.maintenance.bots.portals_merge import PortalsMerge
site = pywikibot.Site()

# page_title = "الشاوية (المغرب)"
page_title = "مستخدم:لوقا/ملعب 24"

page = pywikibot.Page(site, page_title)
# rev_id = 60534506 # some revision id

main_summary = "بوت:صيانة V4.8.10"

obj = PortalsMerge(page, page.text, main_summary)
# obj = PortalsMerge(page, page.getOldVersion(rev_id), main_summary)
text, summary = obj()

page.text = text
page.save(summary)
