import pywikibot

from module import UpdatePage, ArticleTables, index, Database

# Set the parameters for the update
query = """select user_name,
				  (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "rights" and
                    log_params like '%5::newgroups%"bot"%'
                    and log_params not like '%::oldgroups"%"sysop"%5::newgroups%'
                    and log_params not like '%::oldgroups"%"bot"%5::newgroups%') as "+بوت",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights" and
                  log_params like '%5::newgroups%"sysop"%'
                  and log_params not like '%::oldgroups"%"sysop"%5::newgroups%') as "+إداري",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%5::newgroups%"bureaucrat"%'
                  and log_params not like '%::oldgroups"%"bureaucrat"%5::newgroups%') as "+بيروقراط",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%5::newgroups%"accountcreator"%'
                  and log_params not like '%::oldgroups"%"accountcreator"%5::newgroups%') as "+منشئ حسابات",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%5::newgroups%"import"%'
                  and log_params not like '%::oldgroups"%"import"%5::newgroups%') as "+مستورد",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%::oldgroups"%"import"%5::newgroups%'
                  and log_params not like '%5::newgroups%"import"%' ) as "-مستورد",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%::oldgroups"%"accountcreator"%5::newgroups%'
                  and log_params not like '%5::newgroups%"accountcreator"%') as "-منشئ حسابات",

                  (select count(*) from logging
                   inner join actor on actor_id = log_actor
                   where actor_user = user_id and log_type = "rights"  and
                  log_params like '%::oldgroups"%"bot"%5::newgroups%'
                  and log_params not like '%::oldgroups"%"sysop"%5::newgroups%'
                  and log_params not like '%5::newgroups%"bot"%') as "-بوت",

                  (select count(*) from revision
                   inner join actor on actor_id = rev_actor
                   where actor_user = user_id and rev_page = 213729 and
                  rev_minor_edit = 0) as "وب:طصب"
from user
inner join user_groups
on ug_user = user_id
where ug_group = "bureaucrat";"""
file_path = 'stub/activity_of_bureaucrats.txt'
page_name = "ويكيبيديا:إحصاءات/نشاط البيروقراطيين"


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
list_of_categories = create_category_page_for_every_user()
# Create an instance of the ArticleTables class
tables = ArticleTables()


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
    number = 0
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
    ("+بيروقراط", "+بيروقراط"),
    ("+منشئ حسابات", "+منشئ حسابات"),
    ("+مستورد", "+مستورد"),
    ("-مستورد", "-مستورد"),
    ("-منشئ حسابات", "-منشئ حسابات"),
    ("-بوت", "-بوت"),
    ("[[وب:طصب]]", "وب:طصب"),
    ("[[:تصنيف:خلاصة بيروقراط|خ.ب]]", None, total_numbers_in_category),
    ("المجموع", None, total),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
