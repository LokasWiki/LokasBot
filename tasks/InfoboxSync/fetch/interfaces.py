"""Abstract interfaces for the fetch stage."""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from .models import PageInfo
from .observers import FetchObserver, LoggingFetchObserver

logger = logging.getLogger(__name__)


class WikipediaFetcher(ABC):
    """Abstract base class for Wikipedia page fetchers using Template Method."""

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