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
# todo:make it dynimic and add acts of check_usernames task here
year = 2023
month = "مايو"
site = pywikibot.Site()
for item in my_pages_list:
    page_title = item['name'].replace("YEAR", str(year)).replace("MONTH", str(month))
    page = pywikibot.Page(site, page_title)
    if not page.exists():
        page.text = item['template']
        page.save("بوت:إنشاء صفحات مطلوبة V1.0.2")
