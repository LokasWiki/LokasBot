import pywikibot

my_list = [
    "قالب:تشكيلة نادي أتلتيك بيلباو",
    "قالب:تشكيلة أتلتيكو مدريد",
    "قالب:تشكيلة نادي أوساسونا",
    "قالب:تشكيلة نادي إسبانيول",
    "قالب:تشكيلة نادي إشبيلية",
    "قالب:تشكيلة نادي إيبار",
    "قالب:تشكيلة نادي برشلونة",
    "قالب:تشكيلة رايو فايكانو",
    "قالب:تشكيلة نادي إلتشي",
    "قالب:تشكيلة نادي قادش",
    "قالب:تشكيلة نادي خيتافي",
    "قالب:تشكيلة ديبورتيفو ألافيس",
    "قالب:تشكيلة نادي ريال بلد الوليد",
    "قالب:تشكيلة ريال بيتيس",
    "قالب:تشكيلة ريال سوسيداد",
    "قالب:تشكيلة نادي ريال مايوركا",
    "قالب:تشكيلة ريال مدريد",
    "قالب:تشكيلة سلتا فيغو",
    "قالب:تشكيلة نادي غرناطة",
    "قالب:تشكيلة نادي فالنسيا",
    "قالب:تشكيلة نادي فياريال",
    "قالب:تشكيلة نادي ليغانيس",
    "قالب:تشكيلة نادي ليفانتي",
]

site = pywikibot.Site("ar", "wikipedia")
wiki_table = ""
for t_item in my_list:

    ar_page = pywikibot.Page(site, t_item)

    en_title = None
    for item in ar_page.langlinks():
        if str(item).startswith("[[en:"):
            en_title = item.title
            break
    temp_title = t_item.replace("قالب:", "مستخدم:LokasBot/تحديث تشكيلة/")
    title = t_item.replace("قالب:", "")
    wiki_table += """
        |-
        |[[temp_title|title]]
        |[[:en:template:en_title]]

        """.replace("en_title", en_title).replace("temp_title", temp_title).replace("title", title)

print(wiki_table)
#
# bot = BotFactory()
# bot.run(item)

# page = pywikibot.Page(site, item)
# temp_text = page.text
# temp_title = item.replace("قالب:","مستخدم:LokasBot/تحديث تشكيلة/")
# page = pywikibot.Page(site, temp_title)
# page.text = temp_text
# page.save("بوت نسخ")
