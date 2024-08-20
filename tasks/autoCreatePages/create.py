# This script creates a list of page titles with corresponding templates to be used for monthly maintenance tasks on a wiki site.
# The script checks if the current day is the first day of the month and gets the current month and year to be used in the page titles.
# It then creates the pages with the specified templates if they do not already exist on the wiki site.
# The list of page titles and templates to be used are defined in the my_pages_list variable.
import datetime
import logging

import pywikibot

"""
The my_pages_list variable is a list of dictionaries that contains the page titles and templates to be used for monthly maintenance tasks on a wiki site.
Each dictionary in the list has two keys: "name" and "template". The "name" key contains the page title with placeholders for the current month and year,
which will be replaced with the current month and year when the script is run. The "template" key contains the template to be used for the corresponding page title.

Example:
my_pages_list = [
    {"name": "Category:Pages needing translation review since MONTH YEAR", "template": "{{Translation review monthly category}}"},
    {"name": "Category:Pages to be deleted since MONTH YEAR", "template": "{{Monthly cleanup category}}"}
]

In the above example, the first dictionary in the list has a "name" key of "Category:Pages needing translation review 
since MONTH YEAR" and a "template" key of "{{Translation review monthly category}}". When the script is run, the "MONTH" and "YEAR" placeholders 
in the "name" key will be replaced with the current month and year, and a page with the resulting title will be created 
with the template "{{Translation review monthly category}}".
"""
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
    {"name": "تصنيف:مراجعات الزملاء MONTH YEAR", "template": "{{تصنيف مخفي}}"},
]


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


class Create:
    def __init__(self):
        #  get current day
        self.current_day = datetime.datetime.now()
        # get current month
        self.current_month = self.current_day.month
        # get current year
        self.current_year = self.current_day.year
        # get arabic month name
        self.month_name = MonthName(self.current_month).get_month_name()

        self.site = pywikibot.Site()

    def check_day_and_month(self):
        # stop this script if current day not 1
        if self.current_day.day != 1:
            raise Exception("Current day is not 1")
        # stop this script month name is None
        if self.month_name is None:
            raise Exception("Month name is None")

    def page_exists(self, page_title):
        page = pywikibot.Page(self.site, page_title)
        return page.exists()

    def get_page_title(self, page_name_template):
        return page_name_template.replace("YEAR", str(self.current_year)).replace("MONTH", str(self.month_name))

    def create_pages(self, my_pages_list):

        self.check_day_and_month()

        # debug print
        print("Current month is: " + str(self.current_month))
        print("Current year is: " + str(self.current_year))
        print("Month name is: " + self.month_name)

        for item in my_pages_list:
            page_title = self.get_page_title(item['name'])
            page = pywikibot.Page(self.site, page_title)
            if not self.page_exists(page_title):
                page.text = item['template']
                page.save("بوت:إنشاء صفحات مطلوبة V2.1.0")
            else:
                print("Page " + page_title + " is exists")
                logging.info("Page " + page_title + " is exists")


def main():
    create = Create()
    create.create_pages(my_pages_list)


if __name__ == '__main__':
    main()
