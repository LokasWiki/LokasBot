from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT actor_name, COUNT(*) as q_user_editcount
FROM revision r
         INNER JOIN actor ON r.rev_actor = actor.actor_id
         INNER JOIN page p on r.rev_page = p.page_id
WHERE p.page_namespace = 100
  and p.page_is_redirect = 0
  and r.rev_parent_id = 0
  and p.page_title not like "%/%"
  and actor_id NOT IN ("2579643")
  and actor_user not in (137877)
GROUP BY actor_name
having COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 500;"""
file_path = 'stub/users_by_number_of_portals_creation_with_bot.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/المستخدمين حسب عدد إنشاء البوابات (متضمنة البوتات)"


def username(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def total_edits(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    number = format(row['q_user_editcount'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("عدد البوابات", None, total_edits),
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
