import pywikibot

site = pywikibot.Site("ar", "wikipedia")

# page_name2 = "مستخدم:لوقا/ملعب 37"
#
# page2 = pywikibot.Page(site, page_name2)
#
# print(page2.get_parsed_page())
#
# exit()

page_name = "دوال مثلثية"

page = pywikibot.Page(site, page_name)

#
rev = page.getOldVersion(63408845)

print(rev)

#
# replace_text = """== هوامش وملاحظات ==
# {{مراجع|مجموعة=ملاحظة}}
# == مراجع ==
# ;فهرس المراجع
# {{مراجع|محاذاة=نعم}}
# """
#
# rev = rev.replace(replace_text, "")
#
# page2.text = rev
#
# page2.save("تجربة", minor=False, botflag=True)
