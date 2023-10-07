import pywikibot.page

from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select count(page.page_id) as "count_of_cites",iwlinks.iwl_title as "q_iwl_title" from page

inner join templatelinks on page.page_id = templatelinks.tl_from
inner join linktarget on lt_id = tl_target_id

inner join iwlinks on page.page_id = iwlinks.iwl_from
where iwlinks.iwl_title in  (select iwl_title from iwlinks  where iwl_from = 9120840) and lt_title in (
  "استشهاد_بويكي_بيانات",
  "Citeq",
  "Cite_Q"
)
and page.page_namespace = 0 and  lt_namespace = 10
GROUP BY q_iwl_title
order by count_of_cites desc;"""
file_path = 'stub/cite_q.txt'
page_name = "ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات"
# page_name = "مستخدم:لوقا/ملعب 25"



def item(row, result, index):
    name = str(row['q_iwl_title'], 'utf-8')
    return f"[[d:{name}|{name}]]"


def item_title(row, result, index):
    name = str(row['q_iwl_title'], 'utf-8')
    name_of_itme = ""
    try:
        site = pywikibot.Site("wikidata")
        page_item = pywikibot.page.ItemPage(site, name)
        if page_item.isRedirectPage():
            target_page = page_item.getRedirectTarget()
            target_page.get()
            if 'ar' in target_page.labels:
                name_of_itme = target_page.labels['ar']
        else:
            page_item.get()
            if 'ar' in page_item.labels:
                name_of_itme = page_item.labels['ar']

    except:
        print("error to get item from wikdata")

    return name_of_itme


def end_row_in_main(result):
    total = {'count_of_cites': 0}

    for row in result:
        for key in total:
            total[key] += row[key]
    return f"""|- class="sortbottom"\n! colspan="3" | مجمل عدد الاستشهادات\n! style="text-align:center;" | {total['count_of_cites']}\n"""


def header_page(result):
    total = {'count_of_cites': 0}

    for row in result:
        for key in total:
            total[key] += row[key]

    # number of ref in page
    site = pywikibot.Site()
    page = pywikibot.Page(site, "ويكيبيديا:مصادر_موثوقة/معاجم_وقواميس_وأطالس")
    html_page = page.get_parsed_page()
    count_of_ref = html_page.count("↑")

    # top cite used

    top_cite_row = max(result, key=lambda x: x['count_of_cites'])

    tem_header = """{{معاجم وقواميس وأطالس}}
يوجد في صفحة المعاجم أكثر من COUNT_OF_REF معجماً متنوعاً تغطي قرابة 25 فرعاً من فروع المعرفة البشرية.

بدأنا في عام 2023 بتتبع إحصاءات الاستشهادات التي تستعمل قالب {{قا|استشهاد بويكي بيانات}}، وبلغ عددها في {{نسخ:#time:j F Y}} أكثر من COUNT_OF_CITES استشهاد، وكان المعجم الذي اُستشهد به أكثر عدد من المرات هو {{وصلة ويكي بيانات|Q_IWL_TITLE}} بعدد إجمالي من الاستشهادات بلغ TOP_CITE_ROW_COUNT.

يُحدِّث '''BOT_USER_NAME''' محتويات هذه الصفحة آلياً مرة كل أسبوع.
{{تحديد}}

<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%; -moz-border-radius: 0.3em; border-radius: 0.3em;">
<center>
'''حَدَّث BOT_USER_NAME هذه القائمة في :  BOT_TIME_NOW (ت ع م) '''
</center>
</div>
<center>
<div style="background: #E5E4E2; padding: 0.5em; -moz-border-radius: 0.3em; border-radius: 0.3em;">
""".replace("COUNT_OF_CITES", str(total['count_of_cites'])).replace("COUNT_OF_REF", str(count_of_ref)).replace(
        "TOP_CITE_ROW_COUNT", str(top_cite_row['count_of_cites'])).replace("Q_IWL_TITLE",
                                                                           str(top_cite_row['q_iwl_title'], 'utf-8'))
    return tem_header


columns = [
    ("الرقم", None, index),
    ("العنصر", None, item),
    ("اسم الكتاب", None, item_title),
    ("عدد مرات الاستشهاد", "count_of_cites"),
]


def main(*args: str) -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns, header_text=header_page, end_row_text=end_row_in_main)
    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
