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
site = pywikibot.Site("en", "wikipedia")
while True:
    c.execute("select id,en_page from identifiers where exites_in_en is null")
    rows = c.fetchall()
    if len(rows) == 0:
        break
    for row in rows:
        try:
            id = row[0]
            en_page = row[1]
            page = pywikibot.Page(site, en_page)
            print("get page " + en_page)
            if page.exists():
                print("page exist")
                c.execute("update identifiers set exites_in_en = '1' where id = ?", (id,))
            else:
                print("page not exist")
                c.execute("update identifiers set exites_in_en = '0' where id = ?", (id,))
            conn.commit()

        except Exception as e:
            print(e)
            print(row)
