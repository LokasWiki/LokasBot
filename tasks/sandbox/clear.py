import pywikibot

site = pywikibot.Site()
page = pywikibot.Page(site, "ويكيبيديا:ملعب")
text = "{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->"
summary = "بوت:افراغ الصفحة تلقائيا!"
page.text = text
page.save(summary=summary)
