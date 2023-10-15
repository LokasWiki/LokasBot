from tasks.statistics.module import UpdatePage, ArticleTables, index

# https://quarry.wmcloud.org/query/77311#
# Set the parameters for the update
query = """
SELECT distinct
    u.user_name AS user_name,
    MIN(rev.rev_timestamp) AS first_edit_date,
    SUM(CASE WHEN p.page_namespace = 0 AND p.page_is_redirect = 0 THEN 1 ELSE 0 END) AS pages_created,
    SUM(CASE WHEN p.page_namespace = 10 AND p.page_is_redirect = 0 THEN 1 ELSE 0 END) AS template_created,
    SUM(CASE WHEN p.page_namespace = 12 AND p.page_is_redirect = 0 THEN 1 ELSE 0 END) AS help_created,
    SUM(CASE WHEN p.page_namespace = 14 AND p.page_is_redirect = 0 THEN 1 ELSE 0 END) AS category_created,
    SUM(CASE WHEN p.page_namespace = 100 AND p.page_is_redirect = 0 AND p.page_title NOT LIKE '%/%' THEN 1 ELSE 0 END) AS portals_created,
    SUM(CASE WHEN p.page_namespace = 0 AND p.page_is_redirect = 1 THEN 1 ELSE 0 END) AS redirect_created
FROM user u
JOIN actor a ON a.actor_user = u.user_id
JOIN revision rev ON rev.rev_actor = a.actor_id
JOIN page p ON rev.rev_page = p.page_id
WHERE
    ucase(a.actor_name) NOT LIKE ucase('%BOT') COLLATE utf8mb4_general_ci
    AND a.actor_name NOT LIKE '%بوت%' COLLATE utf8mb4_general_ci
    AND a.actor_name NOT IN (SELECT u2.user_name FROM user_groups ug JOIN user u2 ON ug.ug_user = u2.user_id WHERE ug.ug_group = 'bot')
    AND a.actor_id NOT IN ('2579643')
    AND rev.rev_parent_id = 0
    AND a.actor_user NOT IN (137877)
GROUP BY u.user_name
ORDER BY pages_created DESC
LIMIT 500;
"""
file_path = 'stub/users_by_the_number_of_pages_created.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/المستخدمين حسب عدد إنشاء الصفحات"


def username(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def first_edit_date_str(row, result, index):
    first_edit_date = str(row['first_edit_date'], 'utf-8')
    return "{{نسخ:#time:j F Y|" + first_edit_date + "}}"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("أول مساهمة", None, first_edit_date_str),
    ("مقالة", "pages_created"),
    ("قالب", "template_created"),
    ("مساعدة", "help_created"),
    ("تصنيف", "category_created"),
    ("بوابة", "portals_created"),
    ("تحويلة", "redirect_created"),
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
