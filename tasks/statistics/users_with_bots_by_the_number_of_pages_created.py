from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT u.user_name as user_name,
       (
           SELECT MIN(rev_timestamp)
           FROM revision
           WHERE rev_actor = a.actor_id
       ) AS first_edit_date,
       (
           SELECT COUNT(*)
           FROM revision
                    INNER JOIN actor ON rev_actor = actor.actor_id
                    INNER JOIN page  on rev_page = page.page_id
           WHERE page_namespace = 0
             AND page_is_redirect = 0
             AND rev_parent_id = 0
             AND rev_actor = a.actor_id
       ) AS pages_created,
       (
            select COUNT(*)
            FROM revision
                     INNER JOIN actor ON rev_actor = actor.actor_id
                     INNER JOIN page p on rev_page = page_id
            WHERE page_namespace = 10
              and page_is_redirect = 0
              and rev_parent_id = 0
              AND rev_actor = a.actor_id
       ) AS template_created,
       (
            select COUNT(*)
            FROM revision
                     INNER JOIN actor ON rev_actor = actor.actor_id
                     INNER JOIN page p on rev_page = page_id
            WHERE page_namespace = 12
              and page_is_redirect = 0
              and rev_parent_id = 0
              AND rev_actor = a.actor_id
       ) AS help_created,
       (
            select COUNT(*)
            FROM revision
                     INNER JOIN actor ON rev_actor = actor.actor_id
                     INNER JOIN page p on rev_page = page_id
            WHERE page_namespace = 14
              and page_is_redirect = 0
              and rev_parent_id = 0
              AND rev_actor = a.actor_id
       ) AS category_created,
       (
            select COUNT(*)
            FROM revision
                     INNER JOIN actor ON rev_actor = actor.actor_id
                     INNER JOIN page p on rev_page = page_id
            WHERE page_namespace = 100
              and page_is_redirect = 0
              and rev_parent_id = 0
              and page_title not like "%/%"
              AND rev_actor = a.actor_id
       ) AS portals_created,
       (
            select COUNT(*)
            FROM revision
                     INNER JOIN actor ON rev_actor = actor.actor_id
                     INNER JOIN page p on rev_page = page_id
            WHERE page_namespace=0
              and page_is_redirect=1
              and rev_parent_id=0
              AND rev_actor = a.actor_id
       ) AS redirect_created,
      (
           select COUNT(*)
           FROM revision
                    INNER JOIN actor ON rev_actor = actor.actor_id
                    INNER JOIN page p on rev_page = page_id
           WHERE page_namespace = 1
             and page_is_redirect = 0
             and rev_parent_id = 0
             AND rev_actor = a.actor_id
       ) AS take_page_created

FROM user u
         JOIN actor a ON a.actor_user = u.user_id
        where actor_user not in (137877)
ORDER BY pages_created DESC
LIMIT 500;"""
file_path = 'stub/users_with_bots_by_the_number_of_pages_created.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/المستخدمين حسب عدد إنشاء الصفحات (متضمنة البوتات)"


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
    ("صفحة نقاش المقالة", "take_page_created"),
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
