"""Pywikibot implementation of Wikipedia fetcher."""

import logging
from typing import Optional
from .interfaces import WikipediaFetcher
from .models import PageInfo
from .observers import FetchObserver

logger = logging.getLogger(__name__)


class PywikibotFetcher(WikipediaFetcher):
    """Pywikibot implementation of Wikipedia fetcher."""

    def __init__(self, site_name: str,
                 observer: Optional[FetchObserver] = None):
        super().__init__(observer)
        self.site_name = site_name
        self.site = None
        self._initialize_site()

    def get_site_name(self) -> str:
        return self.site_name

    def _initialize_site(self):
        """Initialize pywikibot site - lazy initialization."""
        try:
            import pywikibot
            if self.site is None:
                self.site = pywikibot.Site(self.site_name)
                logger.info(f"Initialized pywikibot site: {self.site_name}")
        except ImportError:
            msg = ("pywikibot is required for Wikipedia operations. "
                   "Install with: pip install pywikibot")
            raise ImportError(msg)

    def _check_page_exists(self, page_title: str) -> PageInfo:
        """Check if page exists on the wiki site."""
        try:
            import pywikibot
            page = pywikibot.Page(self.site, page_title)
            exists = page.exists()
            return PageInfo(
                title=page_title,
                exists=exists,
                content=page.text if exists else None
            )
        except Exception as e:
            logger.error(f"Error checking page existence: {e}")
            return PageInfo(title=page_title, exists=False, error=str(e))

    def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
        """Fetch full page content."""
        # Content is already fetched in _check_page_exists for efficiency
        return page_info

    def _fetch_langlinks(self, page_info: PageInfo) -> PageInfo:
        """Fetch language links (interwiki links)."""
        try:
            import pywikibot
            if page_info.exists:
                page = pywikibot.Page(self.site, page_info.title)
                langlinks = {}
                for langlink in page.langlinks():
                    langlinks[langlink.site.code] = langlink.title
                page_info.langlinks = langlinks
            return page_info
        except Exception as e:
            logger.error(f"Error fetching langlinks: {e}")
            page_info.langlinks = {}
            return page_info