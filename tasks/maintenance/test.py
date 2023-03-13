import pywikibot

from tasks.maintenance.bots.rename_template_parameters import RenameTemplateParameters
from tasks.maintenance.bots.template_redirects import TemplateRedirects

site = pywikibot.Site()

# page_title = "الشاوية (المغرب)"
page_title = "مستخدم:لوقا/ملعب 25"

page = pywikibot.Page(site, page_title)
# rev_id = 60534506 # some revision id

main_summary = "بوت:صيانة V4.8.10"

obj1 = TemplateRedirects(page, page.text, main_summary)
text1, summary1 = obj1()
obj = RenameTemplateParameters(page, text1, main_summary)
# obj = PortalsMerge(page, page.getOldVersion(rev_id), main_summary)
text, summary = obj()

print(text)
#
# page.text = text
# page.save(summary)
