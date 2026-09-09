"""Reusable count of dictionaries listed under معاجم وقواميس وأطالس.

The subject pages (أدب، أطالس، ...) are listed on::

    ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/قائمة

Each subject page documents its dictionaries with ``<ref>`` tags, which render
as ``↑`` backlinks in the parsed HTML. This module loops over every link on the
list page (skipping redirects), counts ``↑`` per page via ``get_parsed_page()``,
and stores the grand total on::

    ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم

That count page holds just the number, so **any wiki page can reuse it** with::

    {{ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم}}

``tasks/statistics/cite_q.py`` calls :func:`update_dictionaries_count_page` at
the start of every update, and :func:`get_dictionaries_count` (cached per
process) for its header text, so the count is refreshed with every update.
The script can also run standalone (it is listed in
``toolforge/jobs/statistics-weekly.sh``).
"""

import datetime

import pywikibot

LIST_PAGE_NAME = "ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/قائمة"
COUNT_PAGE_NAME = (
    "ويكيبيديا:مصادر موثوق بها/معاجم وقواميس وأطالس/إحصائيات/عدد المعاجم"
)
COUNT_SUMMARY = "بوت:تحديث عدد المعاجم"

# Per-process cache so cite_q's header reuses the total computed (and saved)
# by update_dictionaries_count_page() instead of re-parsing ~27 pages.
_cached_total = None


def get_dictionaries_counts(site=None):
    """Return ``(total, details)`` over all list-page links.

    ``details`` is a list of ``(title, arrows, pageid)``. Redirect targets
    are reported as ``("title", None, pageid)`` with reason ``"redirect-skip"``
    and do NOT contribute to the total.
    """
    site = site or pywikibot.Site()
    list_page = pywikibot.Page(site, LIST_PAGE_NAME)
    total = 0
    details = []
    for linked in list_page.linkedPages():
        try:
            if linked.isRedirectPage():
                details.append((linked.title(), "redirect-skip", linked.pageid))
                continue
        except Exception as exc:  # noqa: BLE001
            print(f"warning: redirect check failed for {linked.title()}: {exc!r}")
            details.append((linked.title(), "check-error", None))
            continue
        try:
            html = linked.get_parsed_page()
        except Exception as exc:  # noqa: BLE001
            print(f"warning: parse failed for {linked.title()}: {exc!r}")
            details.append((linked.title(), "parse-error", linked.pageid))
            continue
        arrows = html.count("↑") if html else 0
        total += arrows
        details.append((linked.title(), arrows, linked.pageid))
    return total, details


def get_dictionaries_count(site=None, use_cache=True):
    """Return the grand total, using the per-process cache when available."""
    global _cached_total
    if use_cache and _cached_total is not None:
        return _cached_total
    total, _ = get_dictionaries_counts(site=site)
    _cached_total = total
    return total


def update_dictionaries_count_page(site=None):
    """Recompute the total and save it on COUNT_PAGE_NAME. Return the total."""
    global _cached_total
    site = site or pywikibot.Site()
    total, details = get_dictionaries_counts(site=site)
    _cached_total = total
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"<onlyinclude>{total}</onlyinclude>",
        "<!-- بوت: عدد المعاجم = مجموع أسهم ↑ في كل صفحات القائمة (التحويلات مستثناة).",
        f"آخر تحديث: {stamp}.",
    ]
    for title, arrows, pageid in details:
        lines.append(f"{title} | {arrows} | {pageid}")
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
