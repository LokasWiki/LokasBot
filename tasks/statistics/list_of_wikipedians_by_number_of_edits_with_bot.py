from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT user_name, user_editcount
FROM user
where user_id not in (137877)
ORDER BY user_editcount DESC
LIMIT 500;"""
file_path = 'stub/list_of_wikipedians_by_number_of_edits_with_bot.txt'
page_name = "ويكيبيديا:قائمة الويكيبيديين حسب عدد التعديلات (متضمنة البوتات)"


def username(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def total_edits(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    number = format(row['user_editcount'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("عدد المساهمات", None, total_edits),
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
