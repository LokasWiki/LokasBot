import pywikibot

from tasks.statistics.module import UpdatePage, ArticleTables, index, Database

# Set the parameters for the update
query = """ SELECT 
	user_name,
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%5::newgroups%"bot"%' AND log_params NOT LIKE '%::oldgroups"%"sysop"%5::newgroups%' AND log_params NOT LIKE '%::oldgroups"%"bot"%5::newgroups%' THEN 1 ELSE 0 END) AS "+بوت",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%5::newgroups%"sysop"%' AND log_params NOT LIKE '%::oldgroups"%"sysop"%5::newgroups%' THEN 1 ELSE 0 END) AS "+إداري",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%5::newgroups%"bureaucrat"%' AND log_params NOT LIKE '%::oldgroups"%"bureaucrat"%5::newgroups%' THEN 1 ELSE 0 END) AS "+بيروقراط",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%5::newgroups%"accountcreator"%' AND log_params NOT LIKE '%::oldgroups"%"accountcreator"%5::newgroups%' THEN 1 ELSE 0 END) AS "+منشئ حسابات",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%5::newgroups%"import"%' AND log_params NOT LIKE '%::oldgroups"%"import"%5::newgroups%' THEN 1 ELSE 0 END) AS "+مستورد",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%::oldgroups"%"import"%5::newgroups%' AND log_params NOT LIKE '%5::newgroups%"import"%' THEN 1 ELSE 0 END) AS "-مستورد",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%::oldgroups"%"accountcreator"%5::newgroups%' AND log_params NOT LIKE '%5::newgroups%"accountcreator"%' THEN 1 ELSE 0 END) AS "-منشئ حسابات",
	SUM(CASE WHEN log_type = "rights" AND log_params LIKE '%::oldgroups"%"bot"%5::newgroups%' AND log_params NOT LIKE '%::oldgroups"%"sysop"%5::newgroups%' AND log_params NOT LIKE '%5::newgroups%"bot"%' THEN 1 ELSE 0 END) AS "-بوت",
	
	(SELECT COUNT(*) FROM revision
    INNER JOIN actor ON actor_id = rev_actor
    WHERE actor_user = user_id AND rev_page = 213729 AND rev_minor_edit = 0) AS "وب:طصب"
FROM
    logging, user, actor, user_groups
    where actor_id = log_actor 
    and user_id = ug_user
    AND actor_user = user_id
	AND ug_group = "bureaucrat"
GROUP BY user_name;
"""
file_path = 'stub/activity_of_bureaucrats.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/نشاط البيروقراطيين"


def create_category_page_for_every_user():
    loc = {}
    sql = """select user_name
        from user
        inner join user_groups
        on ug_user = user_id
        where ug_group = "bureaucrat";"""
    database = Database()
    database.query = sql
    database.get_content_from_database()
    site = pywikibot.Site()
    for row in database.result:
        user_name = str(row['user_name'], 'utf-8')
        page = pywikibot.Page(site, f'تصنيف:خلاصة بيروقراط بواسطة {user_name}')
        if not page.exists():
            text = "{{تصنيف ويكيبيديا}}\n{{تصنيف مخفي}}"
            text += f'[[تصنيف:خلاصة بيروقراط|{user_name}]]'
            page.text = text
            page.save("بوت:[[ويكيبيديا:إحصاءات/نشاط البيروقراطيين|ويكيبيديا:إحصاءات/نشاط البيروقراطيين]]")
        # counting the number of sub-pages of category
        cat = pywikibot.Category(site, f'تصنيف:خلاصة بيروقراط بواسطة {user_name}')

        sub_pages = list(cat.members())
        count = len(sub_pages)
        loc[user_name] = count
    # print(loc)
    return loc


# auto call
# todo: make that call from main def and not auto run on import
list_of_categories = create_category_page_for_every_user()


def username(row, result, index):
    username = str(row['user_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "{{مس|" + username + "}}"


def total_numbers_in_category(row, result, index):
    number = 0
    user_name = str(row['user_name'], 'utf-8')
    # to avoid raising any errors
    if user_name in list_of_categories:
        number += list_of_categories[user_name]
    return number


def total(row, result, index):
    user_name = str(row['user_name'], 'utf-8')
    del row['user_name']
    number = sum(row.values())
    # to avoid raising any errors
    if user_name in list_of_categories:
        number += list_of_categories[user_name]
    return number


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("+بوت", "+بوت"),
    ("+إداري", "+إداري"),
    ("+بيروقراطي", "+بيروقراط"),
    ("+منشئ حسابات", "+منشئ حسابات"),
    ("+مستورد", "+مستورد"),
    ("-مستورد", "-مستورد"),
    ("-منشئ حسابات", "-منشئ حسابات"),
    ("-بوت", "-بوت"),
    ("[[ويكيبيديا:طلب صلاحية بوت|طصب]]", "وب:طصب"),
    ("[[:تصنيف:خلاصة بيروقراطي|خ.ب]]", None, total_numbers_in_category),
    ("المجموع", None, total),
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
