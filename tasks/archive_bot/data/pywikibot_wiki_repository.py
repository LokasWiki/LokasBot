"""Pywikibot implementation of :class:`WikiRepository` for archive_bot."""

import datetime
import logging
import re
from typing import List, Optional

import pywikibot

from tasks.archive_bot.domain.repositories.wiki_repository import WikiRepository


class PywikibotWikiRepository(WikiRepository):
    """Wiki repository backed by pywikibot."""

    def __init__(self, site: Optional[pywikibot.Site] = None,
                 max_history: int = 5000, minor_edit: bool = True):
        self.site = site or pywikibot.Site()
        self.max_history = max_history
        self.minor_edit = minor_edit
        self.logger = logging.getLogger(__name__)

    def get_page_text(self, title: str) -> str:
        page = pywikibot.Page(self.site, title)
        if not page.exists():
            return ""
        return page.text

    def page_exists(self, title: str) -> bool:
        return pywikibot.Page(self.site, title).exists()

    def save_page(self, title: str, text: str, summary: str) -> bool:
        try:
            page = pywikibot.Page(self.site, title)
            page.text = text
            page.save(summary=summary, minor=self.minor_edit)
            return True
        except Exception as exc:  # noqa: BLE001 - pywikibot raises many types
            self.logger.error("Failed to save %s: %s", title, exc)
            return False

    def get_old_text(self, title: str,
                     cutoff: datetime.datetime) -> Optional[str]:
        page = pywikibot.Page(self.site, title)
        try:
            # Walk metadata-only (fast) to locate the newest revision at or
            # before the cutoff, matching the legacy PHP history walk.
            target_revid = None
            revisions = page.revisions(reverse=False, content=False,
                                       total=self.max_history)
            for revision in revisions:
                timestamp = revision.get("timestamp")
                if timestamp is not None and timestamp <= cutoff:
                    target_revid = revision.get("revid")
                    break
            if target_revid is None:
                return None
            # Fetch only the single snapshot's content.
            return page.getOldVersion(target_revid) or ""
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to load history for %s: %s", title, exc)
        return None

    def is_sysop_protected(self, title: str) -> bool:
        page = pywikibot.Page(self.site, title)
        try:
            protection = page.protection()
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to read protection for %s: %s", title, exc)
            return False
        edit = protection.get("edit")
        return bool(edit and edit[0] == "sysop")

    def list_archive_counters(self, base_prefix: str) -> List[int]:
        page = pywikibot.Page(self.site, base_prefix)
        namespace = page.namespace()
        prefix = page.title(with_ns=False)
        pattern = re.compile(re.escape(prefix) + r"\s*(\d+)\s*$")

        counters: List[int] = []
        for candidate in self.site.allpages(prefix=prefix, namespace=namespace):
            match = pattern.match(candidate.title(with_ns=False))
            if match:
                counters.append(int(match.group(1)))
        return counters

    def get_transcluded_pages(self, template_title: str,
                              namespace: int) -> List[str]:
        page = pywikibot.Page(self.site, template_title)
        return [p.title() for p in page.embeddedin(namespaces=namespace)]
