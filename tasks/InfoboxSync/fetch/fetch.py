import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PageInfo:
    """Data class for page information."""
    title: str
    exists: bool
    content: Optional[str] = None
    langlinks: Optional[Dict[str, str]] = None
    error: Optional[str] = None


class FetchObserver(ABC):
    """Observer pattern for monitoring fetch operations."""

    @abstractmethod
    def on_page_check_start(self, page_title: str, site: str):
        pass

    @abstractmethod
    def on_page_check_complete(self, page_info: PageInfo):
        pass

    @abstractmethod
    def on_error(self, error: str):
        pass


class LoggingFetchObserver(FetchObserver):
    """Logging implementation of fetch observer."""

    def on_page_check_start(self, page_title: str, site: str):
        logger.info(f"Starting page check for '{page_title}' on {site}")

    def on_page_check_complete(self, page_info: PageInfo):
        if page_info.exists:
            logger.info(f"Page '{page_info.title}' found successfully")
        else:
            logger.warning(f"Page '{page_info.title}' not found")

    def on_error(self, error: str):
        logger.error(f"Fetch error: {error}")


class WikipediaFetcher(ABC):
    """Abstract base class for Wikipedia page fetchers using Template Method pattern."""

    def __init__(self, observer: Optional[FetchObserver] = None):
        self.observer = observer or LoggingFetchObserver()

    def fetch_page_info(self, page_title: str) -> PageInfo:
        """Template method for fetching page information."""
        try:
            self.observer.on_page_check_start(page_title, self.get_site_name())

            page_info = self._check_page_exists(page_title)
            if page_info.exists:
                page_info = self._fetch_page_content(page_info)
                page_info = self._fetch_langlinks(page_info)

            self.observer.on_page_check_complete(page_info)
            return page_info

        except Exception as e:
            error_msg = f"Error fetching page '{page_title}': {str(e)}"
            self.observer.on_error(error_msg)
            return PageInfo(title=page_title, exists=False, error=error_msg)

    @abstractmethod
    def get_site_name(self) -> str:
        pass

    @abstractmethod
    def _check_page_exists(self, page_title: str) -> PageInfo:
        pass

    @abstractmethod
    def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
        pass

    @abstractmethod
    def _fetch_langlinks(self, page_info: PageInfo) -> PageInfo:
        pass


class PywikibotFetcher(WikipediaFetcher):
    """Pywikibot implementation of Wikipedia fetcher."""

    def __init__(self, site_name: str, observer: Optional[FetchObserver] = None):
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
            raise ImportError("pywikibot is required for Wikipedia operations. Install with: pip install pywikibot")

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


class WikipediaSyncFetcher:
    """Main fetcher class using Strategy pattern for different fetch strategies."""

    def __init__(self, observer: Optional[FetchObserver] = None):
        self.observer = observer or LoggingFetchObserver()
        self.ar_fetcher = PywikibotFetcher('ar', self.observer)
        self.en_fetcher = PywikibotFetcher('en', self.observer)

    def fetch_arabic_and_english_pages(self, ar_page_title: str) -> Dict[str, Any]:
        """
        Fetch Arabic page and corresponding English page if it exists.

        Args:
            ar_page_title: Title of the Arabic Wikipedia page

        Returns:
            Dict containing both Arabic and English page information
        """
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
            return {
                'arabic': ar_page_info,
                'english': None,
                'sync_possible': False,
                'error': f"No corresponding English page found for '{ar_page_title}'"
            }

        # Step 3: Fetch English page
        en_page_info = self.en_fetcher.fetch_page_info(en_page_title)

        return {
            'arabic': ar_page_info,
            'english': en_page_info,
            'sync_possible': en_page_info.exists,
            'error': None if en_page_info.exists else f"English page '{en_page_title}' does not exist"
        }

    def _find_english_page_title(self, ar_page_info: PageInfo) -> Optional[str]:
        """Find the corresponding English page title."""
        # Method 1: Check langlinks from Arabic page
        if ar_page_info.langlinks and 'en' in ar_page_info.langlinks:
            return ar_page_info.langlinks['en']

        # Method 2: Try direct title match (for pages with same name in both languages)
        # This is a fallback - in reality you'd want more sophisticated matching
        logger.warning(f"No direct English langlink found for '{ar_page_info.title}', trying direct match")
        return ar_page_info.title


def fetch_wikipedia_data(ar_page_title: str) -> Dict[str, Any]:
    """
    Main function to fetch Wikipedia data for sync operation.

    Args:
        ar_page_title: Arabic page title to sync

    Returns:
        Dictionary with Arabic and English page data
    """
    fetcher = WikipediaSyncFetcher()
    return fetcher.fetch_arabic_and_english_pages(ar_page_title)


# Legacy function for backward compatibility
def fetch_data(url: str) -> dict:
    """
    Legacy function for backward compatibility.
    Now expects a page title instead of URL.
    """
    logger.warning("fetch_data(url) is deprecated. Use fetch_wikipedia_data(page_title) instead.")
    # Extract page title from URL (simple implementation)
    if 'wikipedia.org' in url:
        page_title = url.split('/')[-1].replace('_', ' ')
        return fetch_wikipedia_data(page_title)
    else:
        raise ValueError("URL must be a Wikipedia page URL")