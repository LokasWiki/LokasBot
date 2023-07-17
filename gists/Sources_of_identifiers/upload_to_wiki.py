import sqlite3

import pywikibot
from urlextract import URLExtract

extractor = URLExtract()
db_file_path = "/home/lokas/Downloads/run751073identifiers_v2.sqlite"

# start the connection
conn = sqlite3.connect(db_file_path)

# get the cursor
c = conn.cursor()

# get most common domains and their count from domains table
c.execute("select domain,count from domains order by count desc limit 1000")

site = pywikibot.Site()

page_name = "مستخدم:لوقا/ملعب 36"

page = pywikibot.Page(site, page_name)

wikitable = """
\n{| class="wikitable sortable mw-collapsible"
|+
!#
!عدد مرات الاستخدام
!الموقع
!مثال عشوائي 
!هل ضمن المعرفات 

"""

index = 1

for row in c.fetchall():
    domain = row[0]
    count = row[1]
    url = ""
    try:
        # get example url ftom identifiers table
        c.execute("select url from identifiers where url like  ? order by id limit 1", ("%" + domain + "%",))
        url = c.fetchone()[0]
    except Exception as e:
        print(e)
    if "http" not in url or len(url) == 1:
        wikitable += "\n|-\n| " + str(index) + "\n| " + str(count) + "\n| " + domain + "\n| \n| \n"
    else:
        if "|" in url:
            url = url.split("|")[0]
        new_urls = extractor.find_urls(url)
        if new_urls is None or len(new_urls) == 0:
            wikitable += "\n|-\n| " + str(index) + "\n| " + str(count) + "\n| " + domain + "\n| \n| \n"
        else:
            new_url = new_urls[0]
            wikitable += "\n|-\n| " + str(index) + "\n| " + str(
                count) + "\n| " + domain + "\n| [" + new_url + " 1]\n| \n"
    index += 1

wikitable += "\n|}"

page.text = page.text + wikitable
# page.text =  wikitable

page.save(summary="تحديث", minor=False)
