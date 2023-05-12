import pywikibot
import requests
import wikitextparser as wtp

site = pywikibot.Site()

username_bot = site.username()
# todo: call this from text file and remove from here
# todo: use statistics package and add ability to pass data or get data from db
text = """
<center>
<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%;  -moz-border-radius: 0.3em; border-radius: 0.3em;">
تعرض هذه الصفحة قائمة وصلات حمراء مطلوبة حسب الموضوع ([[TYPE]]).<br/>

'''حَدَّث BOT_USER_NAME هذه القائمة في :  BOT_TIME_NOW (ت ع م) '''
</div>
</center>
<center>
<div style="background: #E5E4E2; padding: 0.5em;   -moz-border-radius: 0.3em; border-radius: 0.3em;">
{| class="wikitable sortable"
!style="background-color:#808080" align="center"|#
!style="background-color:#808080" align="center"|عدد الوصلات
!style="background-color:#808080" align="center"|اسم المقال
TABLE_BODY
|}

</div>
</center>

   """

#  todo:get this list from database ref https://quarry.wmcloud.org/query/73698
list_of_pages = [
    "ألمانيا",
    "إسرائيل",
    "إسلام",
    "إلحاد",
    "إيران",
    "الأردن",
    "الإمارات_العربية_المتحدة",
    "البحرين",
    "الجزائر",
    "السعودية",
    "السودان",
    "الصين",
    "العراق",
    "الكويت",
    "المغرب",
    "المملكة_المتحدة",
    "الهند",
    "الولايات_المتحدة",
    "اليابان",
    "اليمن",
    "باكستان",
    "بوذية",
    "تاريخ",
    "تركيا",
    "تقانة",
    "تلفاز",
    "تونس",
    "الجاينية",
    "جغرافيا",
    "حوسبة",
    "روسيا",
    "رياضيات",
    "الزرادشتية",
    "سلطنة_عمان",
    "سوريا",
    "سيارات",
    "سياسة",
    "السيخية",
    "طب",
    "طيران",
    "علم_الأحياء",
    "علم_الاقتصاد",
    "علم_الفلك",
    "فرنسا",
    "فلسطين",
    "فلسفة",
    "فيزياء",
    "قانون",
    "قطر",
    "كيمياء",
    "لبنان",
    "لعبة_كرة_القدم",
    "ليبيا",
    "المسيحية",
    "مصر",
    "موريتانيا",
    "هندوسية",
    "اليهودية",
]

for type in list_of_pages:
    type = type.replace("_", " ")
    page_name = f"ويكيبيديا:مقالات مطلوبة حسب الاختصاص/{type}"
    # page_name = "مستخدم:لوقا/ملعب 33"

    url = f"https://missingtopics.toolforge.org/?language=ar&project=wikipedia&article=&category={type}&depth=1&wikimode=1&nosingles=1&limitnum=1&doit=Run"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            parsed = wtp.parse(response.text)

            table = parsed.tables[0]

            data = table.data()[1:2001]

            # todo: if title in en try to get page in en wiki and create that by sql query not by api cos every page will have 2000 link
            table_body = ""
            for index, row in enumerate(data):
                table_body += """
                    |-
                    |{}
                    |{}
                    |{}
                    """.format(str(int(index + 1)), row[0], row[1])

            page = pywikibot.Page(site, page_name)
            page.text = str(text).replace("TABLE_BODY", table_body).replace('BOT_USER_NAME',
                                                                            f"[[مستخدم:{username_bot}|{username_bot}]]").replace(
                "BOT_TIME_NOW", "{{نسخ:#time:H:i، j F Y}}").replace("TYPE", type)

            page.save("بوت:تحديث مقالات مطلوبة حسب الاختصاص v1.0.3")
        except:
            # todo: add more log here
            print(f"cand`t work with this page {type}")
