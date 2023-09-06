from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select count(log_id) as "count_of_uploads", actor_name
from logging_userindex 
inner join actor on actor_id = logging_userindex.log_actor
where log_type like "upload"
GROUP BY log_actor
order by count(log_id) desc
limit 500;"""
file_path = 'stub/list_of_wikipedians_by_number_of_files_uploaded.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/قائمة الويكيبيديين حسب عدد الملفات المرفوعة"


def username(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("عدد الملفات المرفوعة", "count_of_uploads"),
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
