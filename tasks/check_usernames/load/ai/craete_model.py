import pywikibot

from core.utils.regex_scanner import RequestsScanner
from core.utils.wikidb import Database
import antispam
d = antispam.Detector("my_model.dat")


db = Database()
db.query = """  SELECT user.user_name AS "username"
  FROM ipblocks
  INNER JOIN user ON ipblocks.ipb_user = user.user_id
  INNER JOIN comment ON ipblocks.ipb_reason_id = comment.comment_id
  WHERE comment.comment_text LIKE "%مستخدم%"
  AND comment.comment_text NOT LIKE "%جوا%"
  limit 30000;"""
db.get_content_from_database()
names = []
for row in db.result:
    name = str(row['username'], 'utf-8')
    print(name.strip().lower())
    d.train(name.strip().lower().replace(" ","_"), True)




db2 = Database()
db2.query = """ SELECT user.user_name AS "username"
 FROM user
 WHERE user.user_id NOT IN (SELECT ipb_user FROM ipblocks)
 limit 30000;"""
db2.get_content_from_database()
names = []
for row in db2.result:
    name = str(row['username'], 'utf-8')
    print(name.strip().lower())
    d.train(name.strip().lower().replace(" ","_"), False)

page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/قائمة الكلمات المخالفة"

site = pywikibot.Site('ar', 'wikipedia')
page = pywikibot.Page(site, page_title)
scanner = RequestsScanner()
words = []
scanner.pattern = r'\* "(?P<word>[^"]*)"'
scanner.scan(page.text)
if scanner.have_requests:
    for request in scanner.requests:
        words.append(request['word'])

for word in words:
    print(word.strip().lower())
    d.train(word.strip().lower().replace(" ","_"), True)


d.save()
