import pywikibot

from core.utils.wikidb import Database

# you site
site = pywikibot.Site()

db = Database()
summery = """بوت: [https://w.wiki/7NGP تحسين مستوي الحماية]"""

# make type edit or move (first start with edit then move)
db.query = """select page_restrictions.*,page_id,page_namespace,page_title,page_is_redirect
from page
join page_restrictions on page_id = pr_page
where pr_type = 'edit'
and pr_level = 'review'
# and pr_expiry not like "infinity"
group by page_id
order by page_namespace asc, page_title asc;
"""
db.get_content_from_database()
rows = db.result
for row in rows:
    # page title must be utf-8 because it get from database in binary format
    page_title = str(row['page_title'], 'utf-8')
    page_namespace = int(row['page_namespace'])
    page_id = row['page_id']
    page_is_redirect = bool(row['page_is_redirect'])
    # get page
    page = pywikibot.Page(source=site, title=page_title, ns=page_namespace)
    # check if it found and not delete
    if page.exists():
        # skip if page is js file because it can't be protected
        if ".js" in page.title():
            continue
        print("get page: " + page.title())
        # get protection of page in it look like this
        # {'edit': ('review', 'infinity'), 'move': ('review', 'infinity')}
        protection = page.protection()
        print(protection)
        # you can do any check to custom protection or you can use this if you want to use default protection
        # if 'edit' in protection and protection['edit'] is not None:
        # wehen will set protector we must set edit and move
        # if you want to set page edit by every one use all and else set custom protection based on you site
        protections = {
            'edit': 'all',
            'move': 'editeditorprotected',
        }
        # then will set protection
        page.protect(
            reason=summery,
            expiry='infinity',
            protections=protections
        )
        # and final we show
        print(page.protection())
