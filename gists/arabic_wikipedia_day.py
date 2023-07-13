import pywikibot

from core.utils.wikidb import Database

sql_query = """select distinct page.page_title from flaggedpages
inner join page on page.page_id = flaggedpages.fp_page_id
where page.page_namespace = 0
and page.page_is_redirect = 0
and flaggedpages.fp_reviewed = 0
and flaggedpages.fp_pending_since is not null
order by flaggedpages.fp_pending_since
limit 1000 
"""

db = Database()
db.query = sql_query
db.get_content_from_database()

page_titles = [str(page['page_title'], 'utf-8') for page in db.result]

# split the list into chunks of 50
chunks = [page_titles[x:x + 50] for x in range(0, len(page_titles), 50)]
site = pywikibot.Site("ar", "wikipedia")
# get the pageviews for each chunk
for chunk, i in enumerate(chunks):
    wiki_title = "ويكيبيديا:يوم ويكيبيديا العربية التاسع عشر/مراجعة تعديلات معلقة/مجموعة {}".format(chunk + 1)
    wiki_table = """{| class="wikitable sortable mw-collapsible"
|+
!#
!اسم المقال
!حالة المراجعه"""
    # add page titles to the wiki table
    for index, page_title in enumerate(i):
        new_index = str(int(index) + 1)
        new_title = "[[{}|{}]]".format(page_title, page_title.replace("_", " "))
        wiki_table += """\n|-\n|{}\n|{}\n|""".format(new_index, new_title)

    wiki_table += "\n|}"
    page = pywikibot.Page(site, wiki_title)
    page.text = wiki_table
    page.save("تحديث القائمة")

    # break
