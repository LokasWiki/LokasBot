"""
Repository interface for Wiki Page operations.

This interface defines the contract for page data access operations,
following the Repository pattern to abstract data access from business logic.
"""

from abc import ABC, abstractmethod
from typing import Optional
from tasks.autoCreatePages.domain.entities.page import Page


class PageRepository(ABC):
    """
    Abstract repository interface for wiki page operations.

    This interface defines the contract for data access operations
    related to wiki pages, allowing for different implementations
    (e.g., Wiki API, mock, test implementations).
    """

    @abstractmethod
    def page_exists(self, title: str) -> bool:
        """
        Check if a page with the given title exists.

        Args:
            title (str): The title of the page to check

        Returns:
            bool: True if the page exists, False otherwise
        """
        pass

    @abstractmethod
    def create_page(self, page: Page) -> None:
        """
        Create a new wiki page.

        Args:
            page (Page): The page entity to create

        Raises:
            Exception: If the page creation fails
        """
        pass

    @abstractmethod
    def get_page_content(self, title: str) -> Optional[str]:
        """
        Get the content of an existing page.

        Args:
            title (str): The title of the page

        Returns:
            Optional[str]: The page content if it exists, None otherwise
        """
        pass

    @abstractmethod
    def update_page(self, page: Page) -> None:
        """
        Update an existing wiki page.

        Args:
            page (Page): The page entity with updated content

        Raises:
            Exception: If the page update fails or page doesn't exist
        """
        pass