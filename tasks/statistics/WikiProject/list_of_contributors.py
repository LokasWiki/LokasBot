from core.utils.helpers import prepare_str
from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select  actor_name as "username", count(rev_actor) as "edit_count",
IF(actor_name in (

  select replace(lt_title,"_"," ") from pagelinks
  join page on page.page_id = pagelinks.pl_from 
  inner join linktarget ON lt_id = pl_target_id
  where page.page_namespace in (4) 
  and page_title like "مشروع_ويكي_العراق/المساهمون"
  and lt_namespace in (2)
  and pl_from_namespace in (4)

), "YES", "NO") as "in_WikiProject"
from revision 
JOIN actor ON actor_id = rev_actor
JOIN user ON user_id = actor_user
where rev_timestamp > DATE_SUB(NOW(), INTERVAL 3 MONTH)
#where rev_timestamp > DATE_SUB(NOW(), INTERVAL 2 DAY)
AND actor_name NOT IN (SELECT user_name FROM user_groups JOIN user ON user_id = ug_user WHERE ug_group = 'bot')
#todo: use join
and rev_page in (
  select page.page_id from page where page.page_namespace in (0)
    and page.page_title in (
         select p0.page_title from categorylinks
         inner join page p0 on p0.page_id = categorylinks.cl_from
         where categorylinks.cl_to like "مقالات_مشروع_ويكي_العراق" and categorylinks.cl_type = "page" and p0.page_namespace in (1) 
    ) 
)
GROUP BY rev_actor
HAVING count(rev_actor) > 20
ORDER BY COUNT(rev_actor) DESC;
"""
file_path = 'WikiProject/stub/list_of_contributors.txt'
page_name = "ويكيبيديا:مشروع ويكي العراق/قائمة المساهمين"


# page_name = "مستخدم:لوقا/قائمة المساهمين"


def username(row, result, index):
    username = str(row['username'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "{{مس|" + username + "}}"


def project_participant(row, result, index):
    template = "{{لون|أحمر|لا}}"
    if prepare_str(row['in_WikiProject']) == prepare_str("YES"):
        template = "{{لون|أخضر|نعم}}"
    return template


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("عدد المساهمات آخر 3 شهور في المشروع", "edit_count"),
    ("مشارك في المشروع؟", None, project_participant),
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
