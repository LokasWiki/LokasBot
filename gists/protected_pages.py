import pywikibot

site = pywikibot.Site()
# db = Database()
summery = """بوت: [https://w.wiki/7NGP تحسين مستوي الحماية]"""

# db.query = """select page_restrictions.*,page_id,page_namespace,page_title,page_is_redirect
# from page
# join page_restrictions on page_id = pr_page
# where pr_type = 'edit'
# and pr_level = 'review'
# # and pr_expiry not like "infinity"
# group by page_id
# order by page_namespace asc, page_title asc;
# """
# db.get_content_from_database()
# rows = db.result
rows = [1]
is_local = True
for row in rows:
    if is_local:
        page_title = "المقال"
        page_namespace = 0
        page_id = None
        page_is_redirect = False
    else:
        page_title = str(row['page_title'], 'utf-8')
        page_namespace = int(row['page_namespace'])
        page_id = row['page_id']
        page_is_redirect = bool(row['page_is_redirect'])
    page = pywikibot.Page(source=site, title=page_title, ns=page_namespace)
    if page.exists():
        print("get page: " + page.title())
        protection = page.protection()
        print(protection)
        # {'edit': ('review', 'infinity'), 'move': ('review', 'infinity')}
        # protection['edit'] = ('sysop', protection['edit'][1])
        # print(protection)
        site.protect(
            page=page,
            protections="edit",
            expiry="infinity",
            reason=summery
        )
        print(site.userinfo['rights'])
        print(site.username())
