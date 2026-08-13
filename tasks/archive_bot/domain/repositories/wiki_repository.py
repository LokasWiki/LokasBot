"""Repository interface for wiki operations in the archive_bot task."""

import datetime
from abc import ABC, abstractmethod
from typing import List, Optional


class WikiRepository(ABC):
    """Abstract interface for wiki operations needed by archive_bot.

    Implementations back the domain use cases with concrete wiki access
    (e.g. pywikibot), while in-memory fakes are used in tests.
    """

    @abstractmethod
    def get_page_text(self, title: str) -> str:
        """Return the current wikitext of ``title`` ('' when missing)."""

    @abstractmethod
    def page_exists(self, title: str) -> bool:
        """Return True when ``title`` exists."""

    @abstractmethod
    def save_page(self, title: str, text: str, summary: str) -> bool:
        """Save ``text`` to ``title`` and return True on success."""

    @abstractmethod
    def get_old_text(self, title: str, cutoff: datetime.datetime) -> Optional[str]:
        """Return the text of the newest revision at or before ``cutoff``.

        Returns ``None`` when no revision is old enough.
        """

    @abstractmethod
    def is_sysop_protected(self, title: str) -> bool:
        """Return True when ``title`` is sysop-protected from editing."""

    @abstractmethod
    def list_archive_counters(self, base_prefix: str) -> List[int]:
        """Return the counters of existing archive pages under ``base_prefix``."""

    @abstractmethod
    def get_transcluded_pages(self, template_title: str, namespace: int) -> List[str]:
        """Return titles of pages in ``namespace`` transcluding ``template_title``."""
