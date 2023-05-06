import pywikibot

site = pywikibot.Site()

page_title = "الخرطوم بحري"
page = pywikibot.Page(site, page_title, ns=14)

print(page.text)
