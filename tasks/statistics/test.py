import pywikibot

site = pywikibot.Site()

page_name = "ويكيبيديا:مصادر_موثوقة/معاجم_وقواميس_وأطالس"

page = pywikibot.Page(site,page_name)
html_page = page.get_parsed_page()
count_of_ref = html_page.count("↑")
print(count_of_ref)