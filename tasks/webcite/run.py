import pywikibot
from tasks.webcite.modules.parsed import Parsed

site = pywikibot.Site()

page_name = "دوناتا أوغسطس"
page = pywikibot.Page(site, page_name)

summary = ""

bot = Parsed(page.text, summary)
new_text, new_summary = bot()

if new_text != page.text:
    page.text = new_text
    page.save(new_summary)
