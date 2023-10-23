import sqlite3

import pywikibot

db_path = "/home/lokas/PycharmProjects/pythonProject3/code/gists/ar_pages_delete_from_en_site/ar_pages_delete_from_en_site.db"

# create sqlite db
conn = sqlite3.connect(db_path)

# create table to store data from csv and check if it exists
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS identifiers
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
          en_page text null,
          date text null,
          ar_page text null,
          namespace text null,
          exites_in_en text null,
          comment text null,
          year text null,
          en_page_without_namespace text null,
          en_first_letter text null,
          ar_first_letter text null    
    )
    ''')

# get all rows that not have exites_in_en value
site = pywikibot.Site("ar", "wikipedia")
c.execute("select id,en_page,ar_page,date from identifiers where exites_in_en is 0")
rows = c.fetchall()
wiki_text = """
    {| class="wikitable sortable"
!style="background-color:#808080" align="center"|الرقم
!style="background-color:#808080" align="center"|الصفحة المحذوفه
!style="background-color:#808080" align="center"|الصفحة العربي
!style="background-color:#808080" align="center"|حذف بتاريخ
"""
index = 1
for row in rows:
    en_page = row[1]
    ar_page = row[2]
    date = row[3]
    temp_text = """            
|-
|index
|en_page
|ar_page
|date

    """
    wiki_text += temp_text.replace("index", str(index)).replace("en_page", "[[:en:" + en_page + "]]").replace("ar_page",
                                                                                                              "[[:" + ar_page + "]]").replace(
        "date", "{{نسخ:#time:j F Y|" + date + "}}")
    index += 1

wiki_text += """\n|}"""

page = pywikibot.Page(site, "مستخدم:فيصل/2/2023")
page.text = wiki_text
page.save("تحديث القائمة")
