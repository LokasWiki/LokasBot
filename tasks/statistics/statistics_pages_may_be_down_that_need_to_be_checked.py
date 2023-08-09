import pywikibot

from tasks.statistics.module import UpdatePage, ArticleTables, index

site = pywikibot.Site()

# Set the parameters for the update
query = """select 
  page.page_id, 
  page.page_title, 
  page.page_namespace, 
  page.page_len, 
  IF(page.page_len < 1000, 'YES', 'NO') as "needed_to_check" 
from 
  categorylinks 
  inner join page on page.page_id = categorylinks.cl_from 
where 
  cl_to like 'إحصاءات_يحدثها_LokasBot' 
  and cl_type like 'page'
  order by page.page_len asc,needed_to_check desc;
  """
file_path = 'stub/ٍstatistics_pages_may_be_down_that_need_to_be_checked.txt'
page_name = "مستخدم:LokasBot/صفحات إحصاءات قد تكون معطلة تحتاج للفحص"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


def page_size(row, result, index) -> str:
    return f"{row['page_len']} بايت"


def needed_to_check(row, result, index) -> str:
    return "{{Y}}" if row['needed_to_check'] == "YES" else "{{N}}"


columns = [
    ("الرقم", None, index),
    ("اسم الصفحة", None, page_name_with_namespace),
    ("حجم الصفحة", None, page_size),
    ("تحتاج للفحص", None, needed_to_check),
]


def main(*args: str) -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
