import datetime

import pywikibot

my_pages_list = [
    {"name": "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:صفحات للحذف منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:صفحات نقاش حذف غير مغلقة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بحاجة لتدقيق خبير منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بحاجة للتحديث منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بحاجة للتقسيم منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بحاجة للتنسيق منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بدون مصدر منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات بها وصلات داخلية قليلة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات ذات عبارات بحاجة لمصادر منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات غير مراجعة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات فيها عبارات متقادمة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات للتدقيق اللغوي منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات مترجمة آليا منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات مطلوب توسيعها منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات يتيمة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:تصنيفات تهذيب منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:تصنيفات تهذيب منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
    {"name": "تصنيف:مقالات غير مصنفة منذ MONTH YEAR", "template": "{{تصنيف تهذيب شهري}}"},
]


# create class to get arbic month name by number of month
class MonthName:
    def __init__(self, month):
        self.month = month

    def get_month_name(self):
        if self.month == 1:
            return "يناير"
        elif self.month == 2:
            return "فبراير"
        elif self.month == 3:
            return "مارس"
        elif self.month == 4:
            return "أبريل"
        elif self.month == 5:
            return "مايو"
        elif self.month == 6:
            return "يونيو"
        elif self.month == 7:
            return "يوليو"
        elif self.month == 8:
            return "أغسطس"
        elif self.month == 9:
            return "سبتمبر"
        elif self.month == 10:
            return "أكتوبر"
        elif self.month == 11:
            return "نوفمبر"
        elif self.month == 12:
            return "ديسمبر"
        else:
            return None


#  get current day
current_day = datetime.datetime.now()

# stop this script if current day not 1
if current_day.day != 1:
    print("Current day is not 1")
    exit()

# get current month
current_month = current_day.month
# get current year
current_year = current_day.year
# get arabic month name
month_name = MonthName(current_month).get_month_name()

#  stop this script month name is None
if month_name is None:
    print("Month name is None")
    exit()

#  debug print
print("Current month is: " + str(current_month))
print("Current year is: " + str(current_year))
print("Month name is: " + month_name)

exit()

site = pywikibot.Site()
for item in my_pages_list:
    page_title = item['name'].replace("YEAR", str(current_year)).replace("MONTH", str(current_month))
    page = pywikibot.Page(site, page_title)
    if not page.exists():
        page.text = item['template']
        page.save("بوت:إنشاء صفحات مطلوبة V1.1.0")
