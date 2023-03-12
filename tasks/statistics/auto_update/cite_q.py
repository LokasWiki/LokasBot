import pywikibot
import wikitextparser as wtp

from tasks.statistics.cite_q import page_name, columns, end_row_in_main, query, file_path, header_page
from core.utils.helpers import prepare_str
from tasks.statistics.module import ArticleTables, UpdatePage


def check(page_title):
    template_name = prepare_str("حدث الصفحة بالبوت")
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)
    status = False
    if page.exists():
        parsed = wtp.parse(page.text)
        for template in parsed.templates:
            if prepare_str(template.name) == template_name:
                for arg in template.arguments:
                    if prepare_str(arg.name) == prepare_str("حدث الصفحة"):
                        if prepare_str(arg.value) == prepare_str("نعم"):
                            status = True
                            break

    return status


def main(*args: str) -> int:
    if check(page_name):

        # Create an instance of the ArticleTables class
        tables = ArticleTables()
        tables.add_table("main_table", columns, header_text=header_page, end_row_text=end_row_in_main)
        # Create an instance of the updater and update the page
        updater = UpdatePage(query, file_path, page_name, tables)
        updater.update()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
