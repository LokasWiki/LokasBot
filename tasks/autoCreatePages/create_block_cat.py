from datetime import datetime

import pywikibot.flow

from tasks.check_usernames.check.modules import DateFormatter

try:
    site = pywikibot.Site()
    formatter = DateFormatter("ar")
    start_date = datetime.now()
    start_time_str = start_date.strftime("%Y%m%d%H%M%S")
    cat_date = formatter.format_timestamp(start_time_str)
    cat_name = f"تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ {cat_date}"
    cat = pywikibot.Category(site, cat_name)
    if not cat.isEmptyCategory():
        cat.text = "{{تصنيف تهذيب شهري}}"
        cat.save("بوت:إنشاء صفحات مطلوبة V1.0.2")
except:
    print("failed to create category")
