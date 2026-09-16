"""Reusable count of dictionaries listed under معاجم وقواميس وأطالس.

The dictionaries themselves are the Wikidata items (``Q…``) recorded as
interwiki links on the data subpages::

    ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/data/1
    ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/data/2
    ...

so the total is simply ``COUNT(DISTINCT Q-id)`` over ``iwlinks`` of every
``data/*`` subpage (``مقدمة`` is an intro page and is skipped). This is the
same ``DATA_SUBPAGES_SUBQUERY`` that ``tasks/statistics/cite_q.py`` uses.

The total is stored on::

    ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم

wrapped in ``<onlyinclude>`` so **any wiki page can reuse just the number** with::

    {{ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم}}

``tasks/statistics/cite_q.py`` calls :func:`update_dictionaries_count_page` at
the start of every update and uses the count page in its header, so the count
is refreshed with every update. The script also runs standalone (it is listed
in ``toolforge/jobs/statistics-weekly.sh``).
"""

import datetime

import pywikibot

from tasks.statistics.module import Database

# Base page: ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/data
# All data/* subpages (e.g. data/1, data/2), except the مقدمة intro page.
DATA_SUBPAGES_SUBQUERY = """
    SELECT page_id FROM page
    WHERE page_namespace = 4
    AND page_title LIKE 'مصادر\\_موثوق\\_بها/معاجم\\_وقواميس\\_وأطالس/إحصائيات/data/%'
    AND page_title != 'مصادر_موثوق_بها/معاجم_وقواميس_وأطالس/إحصائيات/data/مقدمة'
"""

COUNT_PAGE_NAME = (
    "ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم"
)
COUNT_SUMMARY = "بوت:تحديث عدد المعاجم"

# Distinct number of dictionaries (Q-items) across all data/* subpages.
COUNT_QUERY = f"""
SELECT COUNT(DISTINCT REPLACE(iwl_title, 'Special:EntityPage/', '')) AS count_of_items
FROM iwlinks
WHERE iwl_from IN ({DATA_SUBPAGES_SUBQUERY})
"""

# Per data page breakdown (distinct items contributed by each subpage).
BREAKDOWN_QUERY = f"""
SELECT
    p.page_id,
    p.page_title,
    COUNT(DISTINCT REPLACE(iwl.iwl_title, 'Special:EntityPage/', '')) AS count_of_items
FROM page AS p
INNER JOIN iwlinks AS iwl ON iwl.iwl_from = p.page_id
WHERE p.page_id IN ({DATA_SUBPAGES_SUBQUERY})
GROUP BY p.page_id, p.page_title
ORDER BY p.page_title
"""

# Per-process cache so cite_q's header reuses the total computed (and saved)
# by update_dictionaries_count_page() instead of re-querying the replica.
_cached_total = None


def _run_query(query):
    database = Database()
    database.query = query
    database.get_content_from_database()
    return database.result


def get_dictionaries_count(use_cache=True):
    """Return the distinct number of dictionaries on all data/* subpages."""
    global _cached_total
    if use_cache and _cached_total is not None:
        return _cached_total
    result = _run_query(COUNT_QUERY)
    _cached_total = int(result[0]["count_of_items"]) if result else 0
    return _cached_total


def get_dictionaries_breakdown():
    """Return ``[(page_id, title, distinct_count), ...]`` per data subpage."""
    return [
        (row["page_id"], str(row["page_title"], "utf-8"), row["count_of_items"])
        for row in _run_query(BREAKDOWN_QUERY)
    ]


def update_dictionaries_count_page(site=None):
    """Recompute the total and save it on COUNT_PAGE_NAME. Return the total."""
    site = site or pywikibot.Site()
    total = get_dictionaries_count(use_cache=False)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"<onlyinclude>{total}</onlyinclude>",
        "<!-- بوت: عدد المعاجم = عدد المعاجم (عناصر ويكي بيانات) المميزة في كل صفحات data/*،",
        "المحسوب بوصلة COUNT(DISTINCT Q-id) على جدول iwlinks (صفحة المقدمة مستثناة).",
        f"آخر تحديث: {stamp}.",
    ]
    for page_id, title, count in get_dictionaries_breakdown():
        lines.append(f"{title} | {count} | {page_id}")
    lines.append("-->")
    page = pywikibot.Page(site, COUNT_PAGE_NAME)
    page.text = "\n".join(lines)
    page.save(summary=COUNT_SUMMARY)
    return total


def main(*args: str) -> int:
    total = update_dictionaries_count_page()
    print(f"dictionaries count: {total} -> [[{COUNT_PAGE_NAME}]]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
