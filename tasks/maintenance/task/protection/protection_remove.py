import logging

import pywikibot

from core.utils.helpers import check_status
from core.utils.pipeline import Pipeline
from tasks.maintenance.module import get_pages, TASK_SUMMARY, PipelineTasks, clean_summary

custom_query = """select page.page_title as "pl_2_title" from templatelinks
inner join page on templatelinks.tl_from = page.page_id
inner join linktarget on templatelinks.tl_target_id = linktarget.lt_id
where lt_namespace = 10 and lt_title in (
 			"محمية",
            "protected",
            "حماية_خاصة",
            "حماية_نزاع",
            "pp-semi-template",
            "pp-semi-vandalism",
            "pp-dispute",
            "قفل",
            "pp-semi-protected",
            "pp-move-indef",
            "pp-protected",
            "حماية_كلية",
            "حماية_حرب",
            "حماية_جزئية",
            "pp-semi",
            "حماية كاملة",
            "حماية",
            "صفحة_محمية",
            "semi-protection",
            "pp-semi-indef",
            "شبه_محمي",
            "حماية_تخريب"
) and tl_from_namespace in(0)
and page_id not in (select pr_page from page_restrictions )
"""


def main(*args: str) -> int:
    try:
        site = pywikibot.Site()
        time_before_start = 1
        for page_title in get_pages(time_before_start, custom_query=custom_query):
            print("add : " + page_title)
            try:
                page = pywikibot.Page(site, title=page_title, ns=0)
                if page.exists():
                    pipeline = Pipeline(page, page.text, TASK_SUMMARY, PipelineTasks.protection_steps,
                                        PipelineTasks.extra_steps)
                    processed_text, processed_summary = pipeline.process()
                    # write processed text back to the page
                    if pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                        print("start save " + page.title())
                        page.text = processed_text
                        page.save(summary=clean_summary(processed_summary))
                    else:
                        print("page not changed " + page.title())

            except Exception as e:
                logging.error(f"An error occurred while processing: {e}")
                logging.exception(e)

    except Exception as e:
        logging.error("Error occurred while geting pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
