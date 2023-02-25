from core.utils.wikidb import Database

import pywikibot

import antispam

d = antispam.Detector("my_model.dat")



db = Database()
db.query = """select logging.log_title as "q_log_title" from logging
inner join user on user.user_name = logging.log_title
where log_type in ("newusers")
and log_timestamp > DATE_SUB(NOW(), INTERVAL 30 day)
and user.user_id NOT IN (SELECT ipb_user FROM ipblocks)"""
db.get_content_from_database()
names = []
for row in db.result:
    name = str(row['q_log_title'], 'utf-8')
    names.append(name)


page_title = "مستخدم:لوقا/ملعب 20"

site = pywikibot.Site()
page = pywikibot.Page(site, page_title)

text = """<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%; -moz-border-radius: 0.3em; border-radius: 0.3em;">
<center>

أسماء المستخدمين في الأسفل تم التعرف عليها بواسطة البوت كأسماء [[ويكيبيديا:سياسة اسم المستخدم|'''يُحتمل مخالفتها للسياسة''']].

{{ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/رسالة للإداري}}

''قام [[مستخدم:LokasBot|LokasBot]] بتحديث هذه القائمة في : 00:30، 6 ديسمبر 2022 (ت ع م) ''
</div>
<center>
<div style="background: #E5E4E2; padding: 0.5em; -moz-border-radius: 0.3em; border-radius: 0.3em;">
{| class="wikitable sortable"
!style="background-color:#808080" align="center"|الرقم!!style="background-color:#808080" align="center"|نسبة التنبؤ!!style="background-color:#808080" align="center"|المستخدم!!style="background-color:#808080" align="center"|حالة المراجعة!!style="background-color:#808080" align="center"|السبب
|-
"""

num = 1

for name in names:

   try:
       msg1 = name.strip().lower().replace(" ", "_")

       if d.score(msg1) >= 0.6:
           text += """|{0}||{2}||{1}||لا||\n|-
          """.format(num, "{{مس|" + name + "}}", str(d.score(msg1)))
           num += 1
   except:
       text += """|{0}||{2}||{1}||لا||\n|-
              """.format(num, "{{مس|" + name + "}}", "غير معروف")
       num += 1

text += """
|}
[[تصنيف:إدارة ويكيبيديا]]
 """

page.text = text

page.save("بوت:تحديث")
