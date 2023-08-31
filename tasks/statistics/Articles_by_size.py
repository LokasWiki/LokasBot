from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select page_title,page_namespace,page_len from page 
where page_namespace = 0
order by page_len desc
limit 1000 """
file_path = 'stub/Articles_by_size.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/المقالات الأكبر حسب الحجم"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


columns = [
    ("الرقم", None, index),
    ("الاسم", None, page_name_with_namespace),
    ("النطاق", 'page_namespace'),
    ("الحجم", 'page_len'),
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
