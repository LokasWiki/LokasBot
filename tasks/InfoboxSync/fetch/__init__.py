"""Fetch stage module for Wikipedia infobox synchronization."""

import logging
from typing import Dict, Any

from .sync_fetcher import WikipediaSyncFetcher
from .models import PageInfo, SyncResult

logger = logging.getLogger(__name__)

# Main API functions
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


def fetch_sync_result(ar_page_title: str) -> SyncResult:
    """
    Fetch synchronization result with structured return type.

    Args:
        ar_page_title: Title of the Arabic Wikipedia page

    Returns:
        SyncResult object with structured data
    """
    fetcher = WikipediaSyncFetcher()
    return fetcher.fetch_sync_result(ar_page_title)


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


# Expose key classes for advanced usage
__all__ = [
    'WikipediaSyncFetcher',
    'PageInfo',
    'SyncResult',
    'fetch_wikipedia_data',
    'fetch_sync_result',
    'fetch_data'
]