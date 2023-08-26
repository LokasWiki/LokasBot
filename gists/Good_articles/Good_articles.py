import pymysql
import pywikibot
from pywikibot import config as _config

from core.utils.wikidb import Database

query = """
select 
  #concat("[[:en:", page.page_title, "\|",page.page_title,"]]") as "المقال الإنجليزية", 
  page.page_title as "en_title", 
  #page_len as "حجم المقال في النسخة الإنجليزية",
  page_len,
  #concat("[[", ll_title, "]]") as "المقال العربية"
  ll_title as "ar_title"
from 
  categorylinks 
  inner join page on categorylinks.cl_from = page.page_id 
  inner join langlinks on langlinks.ll_from = page.page_id 
where 
  cl_to in ("Good_articles") 
  and cl_type like "page" 
  and page.page_namespace = 0 
  and ll_lang like "ar" 
  and trim(
    coalesce(ll_title, '')
  ) <> ''
  order by page_len desc
"""

db = Database()
db.query = query
db.connection = pymysql.connect(
    host=_config.db_hostname_format.format("enwiki"),
    read_default_file=_config.db_connect_file,
    db=_config.db_name_format.format("enwiki"),
    charset='utf8mb4',
    port=_config.db_port,
    cursorclass=pymysql.cursors.DictCursor,
)
db.get_content_from_database()

db_rows = db.result

# spite every 1000 in group (total 11145)
chunks = [db_rows[x:x + 1000] for x in range(0, len(db_rows), 1000)]
site = pywikibot.Site("ar", "wikipedia")
for i, rows in enumerate(chunks):
    wiki_title = "مستخدم:LokasBot/مقالات جيدة/{}".format(i + 1)
    wiki_text = "{{مستخدم:LokasBot/مقالات جيدة/مقدمة|" + str(i + 1) + "}}"
    wiki_text += """
{| class="wikitable sortable"
|+
! #
!المقال الإنجليزية
!حجم المقال في النسخة الإنجليزية
!المقال العربية

    """
    for index, row in enumerate(rows):
        temp_en_title = "[[:en:{}|{}]]".format(str(row['en_title'], 'utf-8'), str(row['en_title'], 'utf-8'))
        temp_page_size = str(row['page_len'])
        temp_ar_title = "[[{}]]".format(str(row['ar_title'], 'utf-8'))
        wiki_text += """ \n|- \n|{}\n|{}\n|{}\n|{}\n""".format(str(index + 1), temp_en_title, temp_page_size,
                                                               temp_ar_title)
    wiki_text += """\n|}"""

    page = pywikibot.Page(site, wiki_title)
    page.text = wiki_text
    page.save("تحديث القائمة")
