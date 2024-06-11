from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT page.page_title AS ll_page_title,
       linktarget.lt_title AS ll_page_to_title,
       linktarget.lt_namespace AS ll_pl_namespace
FROM page
INNER JOIN pagelinks ON pagelinks.pl_from = page.page_id
inner join linktarget ON lt_id = pl_target_id
WHERE pagelinks.pl_from_namespace = 0
  AND (linktarget.lt_namespace = 2
       OR linktarget.lt_namespace = 3)
  AND page.page_namespace = 0
  AND page.page_is_redirect = 0
  AND page.page_id not in
    (SELECT templatelinks.tl_from
     FROM templatelinks
     JOIN linktarget ON linktarget.lt_id = templatelinks.tl_target_id
     WHERE linktarget.lt_title in
         (SELECT lt_title
          FROM pagelinks
          inner join linktarget ON lt_id = pl_target_id
          WHERE pl_from = 9043549)
       AND templatelinks.tl_from_namespace = 0 )
  AND page.page_title not in
    (SELECT lt_title
     FROM pagelinks
     inner join linktarget ON lt_id = pl_target_id
     WHERE pl_from = 9043549
    );"""
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
