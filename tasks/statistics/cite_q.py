import requests
import pywikibot.page
from pywikibot.comms.http import user_agent

from tasks.statistics.dictionaries_count import (
    COUNT_PAGE_NAME,
    DATA_SUBPAGES_SUBQUERY,
    update_dictionaries_count_page,
)
from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = f"""
SELECT
    COUNT(page.page_id) AS count_of_cites,
    REPLACE(iwlinks.iwl_title, 'Special:EntityPage/', '') AS q_iwl_title
FROM page
INNER JOIN templatelinks ON page.page_id = templatelinks.tl_from
INNER JOIN linktarget ON linktarget.lt_id = templatelinks.tl_target_id
INNER JOIN iwlinks ON page.page_id = iwlinks.iwl_from
WHERE REPLACE(iwlinks.iwl_title, 'Special:EntityPage/', '') IN (
    SELECT REPLACE(iwl_title, 'Special:EntityPage/', '')
    FROM iwlinks
    WHERE iwl_from IN ({DATA_SUBPAGES_SUBQUERY})
)
AND lt_title IN (
    'استشهاد_بويكي_بيانات',
    'Citeq',
    'Cite_Q'
)
AND page.page_namespace = 0
AND lt_namespace = 10
GROUP BY q_iwl_title
ORDER BY count_of_cites DESC;
"""
file_path = 'stub/cite_q.txt'
page_name = "ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات"
# page_name = "مستخدم:لوقا/ملعب 25"



def item(row, result, index):
    name = str(row['q_iwl_title'], 'utf-8')
    return f"[[d:{name}|{name}]]"


# Q-id -> Arabic label, filled in batches by _fetch_item_labels()
_ITEM_LABELS = {}

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"


def _fetch_item_labels(qids):
    """Fill ``_ITEM_LABELS`` for qids using batched wbgetentities calls.

    The old code created a fresh ``ItemPage`` and fetched each entity one by
    one (~600 requests) through pywikibot. While the Wikidata replica lagged
    (``X-Database-Lag`` > ``maxlag``), every request made pywikibot sleep up
    to ``retry_max`` (120 s) per entity, so the update never finished. These
    small read-only lookups are therefore done with plain HTTP, 50 ids per
    request, so Wikidata lag cannot stall the whole statistics update.
    """
    unique_ids = []
    for qid in qids:
        if qid and qid not in _ITEM_LABELS and qid not in unique_ids:
            unique_ids.append(qid)
    if not unique_ids:
        return

    headers = {"User-Agent": user_agent()}
    for start in range(0, len(unique_ids), 50):
        batch = unique_ids[start:start + 50]
        try:
            response = requests.get(
                WIKIDATA_API_URL,
                params={
                    "action": "wbgetentities",
                    "ids": "|".join(batch),
                    "props": "labels",
                    "languages": "ar",
                    "redirects": "yes",
                    "format": "json",
                },
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            print(f"error to get item from wikidata: {exc!r}")
            continue
        entities = data.get("entities", {})
        redirects = {r["from"]: r["to"] for r in data.get("redirects", [])}
        for qid in batch:
            entity = entities.get(redirects.get(qid, qid), {})
            labels = entity.get("labels", {})
            _ITEM_LABELS[qid] = labels.get("ar", {}).get("value", "")


def item_title(row, result, index):
    name = str(row['q_iwl_title'], 'utf-8')
    if name not in _ITEM_LABELS:
        _fetch_item_labels([str(r['q_iwl_title'], 'utf-8') for r in result])
    return _ITEM_LABELS.get(name, "")


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

    # top cite used

    top_cite_row = max(result, key=lambda x: x['count_of_cites'])

    # Reusable count: transclusion of the count page, refreshed by
    # update_dictionaries_count_page() on every run (see main). Any wiki page
    # can reuse it with {{COUNT_PAGE_NAME}}.
    tem_header = """{{معاجم وقواميس وأطالس}}
يوجد في صفحة المعاجم أكثر من {{DICT_COUNT_PAGE}} معجماً متنوعاً تغطي قرابة 25 فرعاً من فروع المعرفة البشرية.

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
""".replace("COUNT_OF_CITES", str(total['count_of_cites'])).replace("DICT_COUNT_PAGE", COUNT_PAGE_NAME).replace(
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
    # Refresh the reusable dictionaries count page on every update, so the
    # {{.../عدد المعاجم}} transclusion above (and on any other wiki page)
    # always shows a fresh total.
    update_dictionaries_count_page()
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns, header_text=header_page, end_row_text=end_row_in_main)
    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
