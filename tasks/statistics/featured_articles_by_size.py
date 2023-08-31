from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select page_namespace,page_title,page_len from categorylinks
inner join page on page.page_id = categorylinks.cl_from
where cl_to like "مقالات_مختارة"
and cl_type like "page"
order by page_len desc"""
file_path = 'stub/featured_articles_by_size.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/المقالات المختارة مرتبة حسب الحجم"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


columns = [
    ("الرقم", None, index),
    ("الاسم", None, page_name_with_namespace),
    ("النطاق", 'page_namespace'),
    ("الحجم", 'page_len'),
    ("عدد الكلمات", None, lambda row, result, index: f"~"),
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
