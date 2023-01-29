import pywikibot
site = pywikibot.Site()
page = pywikibot.Page(site,"عقيد_(رتبة_عسكرية)")
print(page.text)