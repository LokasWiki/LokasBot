from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select page.page_title as ll_page_title,pagelinks.pl_title as ll_page_to_title,pagelinks.pl_namespace as ll_pl_namespace
from page
         inner join pagelinks
                    on pagelinks.pl_from = page.page_id
where pagelinks.pl_from_namespace = 0
  and (pagelinks.pl_namespace = 2 or pagelinks.pl_namespace = 3)
  and page.page_namespace = 0
  and page.page_is_redirect = 0
  and page.page_id not in (select templatelinks.tl_from  from templatelinks
                                                             join linktarget on linktarget.lt_id = templatelinks.tl_target_id
                      where linktarget.lt_title in (select pl_title from pagelinks where  pl_from = 9043549) and templatelinks.tl_from_namespace = 0  )
  and page.page_title not in (select pl_title from pagelinks where  pl_from = 9043549);"""
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
