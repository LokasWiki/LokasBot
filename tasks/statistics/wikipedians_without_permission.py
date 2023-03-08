from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT actor_name AS user_name, date(user_registration) AS user_registration,
        user_editcount AS total_edits,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_deleted = 0) AS live_edits,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp > DATE_SUB(NOW(), INTERVAL 1 MONTH)) AS edits_last_month
FROM actor
         join user on actor_user = user_id
         LEFT JOIN ipblocks ON actor_user = ipb_user
         LEFT JOIN user_groups ON actor_user = ug_user
WHERE ipb_user IS NULL AND ug_user IS NULL
HAVING live_edits >= 400
       AND edits_last_month >= 10;"""
file_path = 'stub/wikipedians_without_permission.txt'
page_name = "ويكيبيديا:قائمة الويكيبيديين بلا صلاحيات"


def username(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def user_registration(row, result, index):
    return row['user_registration']


def live_edits(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    number = format(row['live_edits'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


def total_edits(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    number = format(row['total_edits'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


def edits_last_month(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    number = format(row['edits_last_month'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("تاريخ التسجيل", None, user_registration),
    ("عدد المساهمات", None, live_edits),
    ("عدد المساهمات الحية", None, total_edits),
    ("عدد المساهمات خلال 30 يوم", None, edits_last_month),
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
