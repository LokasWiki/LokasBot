import copy

import pywikibot
import wikitextparser as wtp
from core.utils.wikidb import Database
site = pywikibot.Site()
print("start")
db = Database()
db.query = """select page.page_title,page.page_namespace from templatelinks
inner join page on templatelinks.tl_from = page.page_id
inner join linktarget on templatelinks.tl_target_id = linktarget.lt_id
where lt_namespace = 10 and lt_title = "أعلام_الأزمة_السورية" and tl_from_namespace in(0)
"""
db.get_content_from_database()
for row in db.result:
    page_title = str(row['page_title'],'utf-8')
    page_namespace = int(row['page_namespace'])

    page = pywikibot.Page(site, page_title, ns=page_namespace)
    old_template_name = "أعلام الأزمة السورية"
    new_template_name = "مستخدم:أفرام/ملعب 2"
    parsed = wtp.parse(page.text)
    page_text = page.text
    print("\n== [[" + page_title + "]] ==\n")
    for template in parsed.templates:
        if template.name.strip().lower().replace(" ","_") == str(old_template_name).strip().lower().replace(" ","_"):
            # temp_template = wtp.Template(str(template).replace(":","|").replace("/","|").replace('\\',"|"))
            # temp_template.name = new_template_name
            #
            # print("* <nowiki>"+str(template)+" -> "+str(temp_template)+"</nowiki> ")
            # print(temp_template)

            page_text = page_text.replace(str(template), "")

    if page.text != page_text:
        page.text = page_text
        page.save(
            summary="بوت:[[ويكيبيديا:طلبات إزالة (بوابة، تصنيف، قالب)]] حذف [[قالب:" + old_template_name + "]]"
        )
