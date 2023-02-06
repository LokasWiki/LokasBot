
import re

import pywikibot
import os, sys
import pywikibot

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core import PageProcessor,RequestsPage,RequestsScanner,Query

db = Query()

# Create an instance of the RequestsPage class
site = pywikibot.Site()
site2 = pywikibot.Site("ar", "wikipedia")

type_of_request = 2

pages = db.get_new_pages(100,type_of_request)


#
# for page in pages:
#     print(page)

"""

page_title = "الأرشيدوقة ماريا آنا من النمسا"
page_new_title = "الأرشيدوقة ماريا آنا من النمسا (1610-1665)"

page = pywikibot.Page(site, page_title)

gen = page.backlinks(follow_redirects=False, namespaces=[0, 14, 10, 6], content=True)

for p in gen:
    print(p.title())
    text = str(p.text)
    reg_str = r"\[\[(" + re.escape(page_title) + r")(\|(?:.*?))?\]\]"
    print(reg_str)
    link_list = re.findall(reg_str, text)
    # if link_list:
    for r in link_list:
        print(r)
        r_link = r[0]
        r_title = r[1]
        if r_title == '':
            r_title = "|" + r_link
        old_link = "[[" + r[0] + r[1] + "]]"
        new_link = "[[" + page_new_title + r_title + "]]"
        print(old_link)
        print(new_link)
        text = text.replace(old_link, new_link)

    p.text = text
    # print(text)
    p.save(
        summary="بوت:[[ويكيبيديا:طلبات استبدال الوصلات]] استبدال [[" + page_title + "]] ب [[" + page_new_title + "]]")
        
"""