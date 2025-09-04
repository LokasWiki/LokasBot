"""Main synchronization fetcher using Strategy pattern."""

import logging
from typing import Dict, Any, Optional
from .models import PageInfo, SyncResult
from .observers import FetchObserver, LoggingFetchObserver
from .pywikibot_fetcher import PywikibotFetcher

logger = logging.getLogger(__name__)


class WikipediaSyncFetcher:
    """Main fetcher class using Strategy pattern."""

    def __init__(self, observer: Optional[FetchObserver] = None):
        self.observer = observer or LoggingFetchObserver()
        self.ar_fetcher = PywikibotFetcher('ar', self.observer)
        self.en_fetcher = PywikibotFetcher('en', self.observer)

    def fetch_arabic_and_english_pages(self,
                                       ar_page_title: str) -> Dict[str, Any]:
        """Fetch Arabic page and corresponding English page."""
        logger.info(f"Starting sync fetch for Arabic page: {ar_page_title}")

        # Step 1: Check Arabic page
        ar_page_info = self.ar_fetcher.fetch_page_info(ar_page_title)

        if not ar_page_info.exists:
            return {
                'arabic': ar_page_info,
                'english': None,
                'sync_possible': False,
                'error': f"Arabic page '{ar_page_title}' does not exist"
            }

        # Step 2: Find corresponding English page
        en_page_title = self._find_english_page_title(ar_page_info)

        if not en_page_title:
            error_msg = (
                f"No corresponding English page found for '{ar_page_title}'"
            )
            return {
                'arabic': ar_page_info,
                'english': None,
                'sync_possible': False,
                'error': error_msg
            }

        # Step 3: Fetch English page
        en_page_info = self.en_fetcher.fetch_page_info(en_page_title)

        error_msg = None
        if not en_page_info.exists:
            error_msg = f"English page '{en_page_title}' does not exist"

        return {
            'arabic': ar_page_info,
            'english': en_page_info,
            'sync_possible': en_page_info.exists,
            'error': error_msg
        }

    def _find_english_page_title(self,
                                 ar_page_info: PageInfo) -> Optional[str]:
        """Find the corresponding English page title."""
        # Method 1: Check langlinks from Arabic page
        if ar_page_info.langlinks and 'en' in ar_page_info.langlinks:
            return ar_page_info.langlinks['en']

        # Method 2: Try direct title match
        # This is a fallback - in reality you'd want more sophisticated
        # matching
        msg = f"No direct English langlink found for '{ar_page_info.title}'"
        logger.warning(f"{msg}, trying direct match")
        return ar_page_info.title

    def fetch_sync_result(self, ar_page_title: str) -> SyncResult:
        """Fetch synchronization result with structured return type."""
        result = self.fetch_arabic_and_english_pages(ar_page_title)

        return SyncResult(
            arabic=result['arabic'],
            english=result['english'],
            sync_possible=result['sync_possible'],
            error=result['error']
        )