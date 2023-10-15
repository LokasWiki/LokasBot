from tasks.statistics.module import UpdatePage, ArticleTables, index
# https://quarry.wmcloud.org/query/77305
# Set the parameters for the update
query = """select p.page_title as ll_page_title, pl.pl_title as ll_page_to_title, pl.pl_namespace as ll_pl_namespace
from page p
inner join pagelinks pl on pl.pl_from = p.page_id
where pl.pl_from_namespace = 0
and pl.pl_namespace in (2, 3)
and p.page_namespace = 0
and p.page_is_redirect = 0
and not exists (
    select 1
    from templatelinks tl
    join linktarget lt on lt.lt_id = tl.tl_target_id
    where lt.lt_title in (select pl_title from pagelinks where pl_from = 9043549)
    and tl.tl_from = p.page_id
    and tl.tl_from_namespace = 0
)
and not exists (
    select 1
    from pagelinks pl2
    where pl2.pl_title = p.page_title
    and pl2.pl_from = 9043549
);
"""
file_path = 'stub/articles_in_which_there_is_a_link_to_user_pages.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/مقالات يوجد فيها وصلة إلى صفحات المستخدمين"



def page_title(row, result, index):
    username = str(row['ll_page_title'], 'utf-8')
    name = username
    return "[[" + username + "]]"

def username(row, result,index):
    username = str(row['ll_page_to_title'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    if row['ll_pl_namespace'] == 2:
        page_prefix = 'مستخدم:'
    else:
        page_prefix = 'نقاش المستخدم:'
    return "[["+page_prefix + username + "|" + name + "]]"


columns = [
    ("الرقم", None, index),
    ("المقالة", None, page_title),
    ("الرابط المقصود",None, username),
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
