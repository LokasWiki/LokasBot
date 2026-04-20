"""Observer pattern implementation for monitoring fetch operations."""

import logging
from abc import ABC, abstractmethod
from .models import PageInfo

logger = logging.getLogger(__name__)


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


class MetricsFetchObserver(FetchObserver):
    """Metrics collection implementation of fetch observer."""

    def __init__(self):
        self.metrics = {
            'pages_checked': 0,
            'pages_found': 0,
            'pages_not_found': 0,
            'errors': 0
        }

    def on_page_check_start(self, page_title: str, site: str):
        self.metrics['pages_checked'] += 1

    def on_page_check_complete(self, page_info: PageInfo):
        if page_info.exists:
            self.metrics['pages_found'] += 1
        else:
            self.metrics['pages_not_found'] += 1

    def on_error(self, error: str):
        self.metrics['errors'] += 1

    def get_metrics(self) -> dict:
        """Get current metrics."""
        return self.metrics.copy()