import logging
import traceback

import pywikibot
from pywikibot import pagegenerators


from tasks.maintenance.module import check_status, Pipeline,PipelineTasks,clean_summary,TASK_SUMMARY

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
        try:
            if page.exists() and (not page.isRedirectPage()):
                text = page.text
                pipeline = Pipeline(page, text, TASK_SUMMARY, PipelineTasks.portals_merge_steps, PipelineTasks.extra_steps)
                processed_text, processed_summary = pipeline.process()
                # write processed text back to the page
                if pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                    logging.info("start save " + page.title())
                    page.text = processed_text
                    page.save(summary=clean_summary(processed_summary))
                else:
                    logging.info("page not changed " + page.title())

        except Exception as e:
            logging.error(f"An error occurred while processing: {e}")
            logging.exception(e)
