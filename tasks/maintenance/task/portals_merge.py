import traceback

import pywikibot
from pywikibot import pagegenerators

from tasks.maintenance.bots.dead_end import DeadEnd
from tasks.maintenance.bots.rename_template_parameters import RenameTemplateParameters
from tasks.maintenance.bots.template_redirects import TemplateRedirects
from tasks.maintenance.bots.underlinked import UnderLinked
from tasks.maintenance.bots.unreferenced import Unreferenced
from tasks.maintenance.module import check_status, Pipeline

# bots
from tasks.maintenance.bots.unreviewed_article import UnreviewedArticle
from tasks.maintenance.bots.has_categories import HasCategories
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.maintenance.bots.orphan import Orphan
from tasks.maintenance.bots.stub import Stub

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
            PortalsBar,
            Unreferenced,
            Orphan,
            DeadEnd,
            UnderLinked,
            PortalsMerge,
            PortalsBar,
            Stub
        ]
        extra_steps = [
            TemplateRedirects,
            RenameTemplateParameters
        ]
        try:
            if page.exists() and (not page.isRedirectPage()):
                text = page.text
                summary = "بوت:صيانة V5.6.0"
                pipeline = Pipeline(page, text, summary, steps, extra_steps)
                processed_text, processed_summary = pipeline.process()
                # write processed text back to the page
                if pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                    print("start save " + page.title())
                    page.text = processed_text
                    # to remove duplicate summary
                    if str(processed_summary).count("، تعريب"):
                        processed_summary = str(processed_summary).replace("، تعريب", "")
                        processed_summary += "، تعريب"

                    page.save(summary=processed_summary)
                else:
                    print("page not changed " + page.title())

        except Exception as e:
            print(f"An error occurred while processing {page.title()}: {e}")
            just_the_string = traceback.format_exc()
            print(just_the_string)
