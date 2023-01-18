import pywikibot

from core.check import  CheckPage

site = pywikibot.Site()

check = CheckPage(site)
check.title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت"
check.load_page()
if check.run():
    # start send alert
    print("start send alert")
else:
    print("can`t run page without yes word")
