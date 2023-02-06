
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

requests = db.get_requests(10,type_of_request,1)

for request in requests:

    page_title = request['from_title']
    page_new_title = request['to_title']

    pages = db.get_new_pages(100,request['id'])

    for page in pages:
        p = pywikibot.Page(site2,page['title'],ns=page['namespace'])
        text = str(p.text)
        reg_str = r"\[\[(" + re.escape(page_title) + r")(\|(?:.*?))?\]\]"
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
        db.delete_page(page['id'])
