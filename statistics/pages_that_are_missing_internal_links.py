from module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT p.page_title as ll_page_title, p.page_len as ll_page_len, a.actor_name as ll_user_name
FROM page p
         LEFT JOIN pagelinks pl ON p.page_id = pl.pl_from
         INNER JOIN revision r ON p.page_id = r.rev_page
         INNER JOIN actor a ON r.rev_actor = a.actor_id
WHERE pl.pl_from IS NULL AND p.page_is_redirect = 0 AND p.page_namespace = 0
  AND r.rev_id = (SELECT MIN(rev_id) FROM revision WHERE rev_page = p.page_id)"""
file_path = 'stub/pages_that_are_missing_internal_links.txt'
page_name = "ويكيبيديا:إحصاءات/مقالات بدون وصلات داخلية"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def username(row, result, index):
    ll_user_name = str(row['ll_user_name'], 'utf-8')
    # name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return f"[[user:{ll_user_name}|{ll_user_name}]] ([[نقاش المستخدم:{ll_user_name}|نقاش]])"


def page_title(row, result, index):
    username = str(row['ll_user_name'], 'utf-8')
    name = username
    return "[[" + username + "|" + name + "]]"


def page_history(row, result, index):
    page_title = str(row['ll_user_name'], 'utf-8')
    return f'[http://ar.wikipedia.org/w/index.php?title={page_title}&action=history تاريخ]'


columns = [
    ("الرقم", None, index),
    ("المقالة", None, page_title),
    ("تاريخ الصفحة", None, page_history),
    ("الحجم (كيلوبايت)", "ll_page_len"),
    ("أول مساهم", None, username),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
