import traceback

import pywikibot
from pywikibot import pagegenerators

from tasks.maintenance.module import check_status, Pipeline

# bots
from tasks.maintenance.bots.unreviewed_article import UnreviewedArticle
from tasks.maintenance.bots.has_categories import HasCategories
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.maintenance.bots.orphan import Orphan

site = pywikibot.Site()

list_of_pages = []

categories_names = [
    "تصنيف:صفحة تستعمل قالب بوابة من دون شريط",
    "تصنيف:صفحات_تحتوي_بوابات_مكررة_باستخدام_قالب_بوابة",
    "تصنيف:مقالات_تحتوي_بوابات_مكررة"
]

for cat in categories_names:
    cat_obj = pywikibot.Category(site, cat)
    gen = pagegenerators.CategorizedPageGenerator(category=cat_obj,namespaces=[0])
    for page in gen:
        steps = [
            UnreviewedArticle,
            HasCategories,
            PortalsMerge,
            PortalsBar,
            # Unreferenced,
            Orphan,
            # DeadEnd,
            # Underlinked
        ]
        extra_steps = [

        ]
        try:
            if page.exists() and (not page.isRedirectPage()):
                text = page.text
                summary = "بوت:صيانة V4.8.6"
                pipeline = Pipeline(page, text, summary, steps, extra_steps)
                processed_text, processed_summary = pipeline.process()
                # write processed text back to the page
                if pipeline.hasChange() and check_status():
                    print("start save " + page.title())
                    page.text = processed_text
                    page.save(summary=processed_summary)
                else:
                    print("page not changed " + page.title())
        except Exception as e:
            print(f"An error occurred while processing {page.title()}: {e}")
            just_the_string = traceback.format_exc()
            print(just_the_string)
