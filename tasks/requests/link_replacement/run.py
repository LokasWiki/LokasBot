import re

import pywikibot

from module import  Query,RequestsPage,RequestsScanner,PageProcessor

site = pywikibot.Site()

requests_query = Query('requests.db')

request = requests_query.pop_request()

print(request)


page_title = "الأرشيدوقة ماريا آنا من النمسا"
page_new_title = "الأرشيدوقة ماريا آنا من النمسا (1610-1665)"

page = pywikibot.Page(site, page_title)

gen = page.backlinks(follow_redirects=False, namespaces=[0, 14, 10, 6], content=True)

for p in gen:
    print(p.title())
    text = str(p.text)
    reg_str = "\[\[(" + re.escape(page_title) + ")(\|(?:.*?))?\]\]"
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