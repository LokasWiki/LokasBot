import time

import pywikibot.page

from module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select count(page.page_id) as "count_of_cites",iwlinks.iwl_title as "q_iwl_title" from page

inner join templatelinks on page.page_id = templatelinks.tl_from
inner join linktarget on lt_id = tl_target_id

inner join iwlinks on page.page_id = iwlinks.iwl_from
where iwlinks.iwl_title in  (select iwl_title from iwlinks  where iwl_from = 9119754) and lt_title in (
  "استشهاد_بويكي_بيانات",
  "Citeq",
  "Cite_Q"
)
and page.page_namespace = 0
GROUP BY q_iwl_title;"""
file_path = 'stub/cite_q.txt'
page_name = "ويكيبيديا:مصادر موثوقة/معاجم وقواميس وأطالس/إحصائيات"

# Get the current time and day of the week
current_time = time.localtime()
day_of_week = current_time.tm_wday


# Check if it's fri
if day_of_week == 4:

    # Create an instance of the ArticleTables class
    tables = ArticleTables()


    def item(row, result, index):
        name = str(row['q_iwl_title'], 'utf-8')
        return f"[[d:{name}|{name}]]"


    def item_title(row, result, index):
        name = str(row['q_iwl_title'], 'utf-8')
        name_of_itme = ""
        try:
            site = pywikibot.Site("wikidata")
            page_item = pywikibot.page.ItemPage(site, name)
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
        return f"""\n|- class="sortbottom"\n! colspan="3" | عدد الاستشهادات الكلي\n! style="text-align:center;" | {total['count_of_cites']}\n"""


    columns = [
        ("الرقم", None, index),
        ("العنصر", None, item),
        ("اسم الكتاب", None, item_title),
        ("عدد مرات الاستشهاد", "count_of_cites"),
    ]

    tables.add_table("main_table", columns,end_row_text=end_row_in_main)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
