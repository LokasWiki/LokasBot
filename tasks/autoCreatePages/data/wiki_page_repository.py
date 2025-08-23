"""
Concrete implementation of PageRepository using pywikibot.

This repository implementation handles all wiki page operations
through the pywikibot library, implementing the PageRepository interface.
"""

import logging
from typing import Optional
import pywikibot

from tasks.autoCreatePages.domain.repositories.page_repository import (
    PageRepository
)
from tasks.autoCreatePages.domain.entities.page import Page


class WikiPageRepository(PageRepository):
    """
    Wiki page repository implementation using pywikibot.

    This class provides concrete implementations of all page operations
    defined in the PageRepository interface, using pywikibot for
    actual wiki interactions.
    """

    def __init__(self, site: pywikibot.Site):
        """
        Initialize the WikiPageRepository.

        Args:
            site (pywikibot.Site): The pywikibot site object to use
                for operations
        """
        self.site = site
        self.logger = logging.getLogger(__name__)

    def page_exists(self, title: str) -> bool:
        """
        Check if a page with the given title exists.

        Args:
            title (str): The title of the page to check

        Returns:
            bool: True if the page exists, False otherwise
        """
        try:
            page = pywikibot.Page(self.site, title)
            exists = page.exists()
            self.logger.debug(f"Page existence check for '{title}': {exists}")
            return exists
        except Exception as e:
            error_msg = f"Error checking page existence for '{title}': {e}"
            self.logger.error(error_msg)
            return False

    def create_page(self, page: Page) -> None:
        """
        Create a new wiki page.

        Args:
            page (Page): The page entity to create

        Raises:
            Exception: If the page creation fails
        """
        try:
            wiki_page = pywikibot.Page(self.site, page.title)
            wiki_page.text = page.content
            wiki_page.save(page.creation_message)
            self.logger.info(f"Successfully created page: {page.title}")
        except Exception as e:
            error_msg = f"Failed to create page '{page.title}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def get_page_content(self, title: str) -> Optional[str]:
        """
        Get the content of an existing page.

        Args:
            title (str): The title of the page

        Returns:
            Optional[str]: The page content if it exists, None otherwise
        """
        try:
            if not self.page_exists(title):
                self.logger.debug(f"Page does not exist: {title}")
                return None

            page = pywikibot.Page(self.site, title)
            content = page.text
            self.logger.debug(f"Retrieved content for page: {title}")
            return content
        except Exception as e:
            self.logger.error(f"Error getting content for page '{title}': {e}")
            return None

    def update_page(self, page: Page) -> None:
        """
        Update an existing wiki page.

        Args:
            page (Page): The page entity with updated content

        Raises:
            Exception: If the page update fails or page doesn't exist
        """
        try:
            if not self.page_exists(page.title):
                error_msg = f"Cannot update non-existent page: {page.title}"
                self.logger.error(error_msg)
                raise Exception(error_msg)

            wiki_page = pywikibot.Page(self.site, page.title)
            wiki_page.text = page.content
            wiki_page.save(page.creation_message)
            self.logger.info(f"Successfully updated page: {page.title}")
        except Exception as e:
            if "Cannot update non-existent page" in str(e):
                raise  # Re-raise the specific error
            error_msg = f"Failed to update page '{page.title}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)