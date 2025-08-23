"""
Concrete implementation of CategoryRepository using pywikibot.

This repository implementation handles all wiki category operations
through the pywikibot library, implementing the CategoryRepository interface.
"""

import logging
from typing import Optional
import pywikibot

from tasks.autoCreatePages.domain.repositories.category_repository import (
    CategoryRepository
)
from tasks.autoCreatePages.domain.entities.category import Category


class WikiCategoryRepository(CategoryRepository):
    """
    Wiki category repository implementation using pywikibot.

    This class provides concrete implementations of all category operations
    defined in the CategoryRepository interface, using pywikibot for
    actual wiki interactions.
    """

    def __init__(self, site: pywikibot.Site):
        """
        Initialize the WikiCategoryRepository.

        Args:
            site (pywikibot.Site): The pywikibot site object to use
                for operations
        """
        self.site = site
        self.logger = logging.getLogger(__name__)

    def category_exists(self, name: str) -> bool:
        """
        Check if a category with the given name exists.

        Args:
            name (str): The name of the category to check

        Returns:
            bool: True if the category exists, False otherwise
        """
        try:
            category = pywikibot.Category(self.site, name)
            exists = category.exists()
            self.logger.debug(f"Category existence check for '{name}': {exists}")
            return exists
        except Exception as e:
            error_msg = f"Error checking category existence for '{name}': {e}"
            self.logger.error(error_msg)
            return False

    def create_category(self, category: Category) -> None:
        """
        Create a new wiki category.

        Args:
            category (Category): The category entity to create

        Raises:
            Exception: If the category creation fails
        """
        try:
            wiki_category = pywikibot.Category(self.site, category.name)
            wiki_category.text = category.template
            wiki_category.save(category.creation_message)
            self.logger.info(f"Successfully created category: {category.name}")
        except Exception as e:
            error_msg = f"Failed to create category '{category.name}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def get_category_content(self, name: str) -> Optional[str]:
        """
        Get the content of an existing category.

        Args:
            name (str): The name of the category

        Returns:
            Optional[str]: The category content if it exists, None otherwise
        """
        try:
            if not self.category_exists(name):
                self.logger.debug(f"Category does not exist: {name}")
                return None

            category = pywikibot.Category(self.site, name)
            content = category.text
            self.logger.debug(f"Retrieved content for category: {name}")
            return content
        except Exception as e:
            self.logger.error(f"Error getting content for category '{name}': {e}")
            return None

    def update_category(self, category: Category) -> None:
        """
        Update an existing wiki category.

        Args:
            category (Category): The category entity with updated content

        Raises:
            Exception: If the category update fails or category doesn't exist
        """
        try:
            if not self.category_exists(category.name):
                error_msg = f"Cannot update non-existent category: {category.name}"
                self.logger.error(error_msg)
                raise Exception(error_msg)

            wiki_category = pywikibot.Category(self.site, category.name)
            wiki_category.text = category.template
            wiki_category.save(category.creation_message)
            self.logger.info(f"Successfully updated category: {category.name}")
        except Exception as e:
            if "Cannot update non-existent category" in str(e):
                raise  # Re-raise the specific error
            error_msg = f"Failed to update category '{category.name}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def is_empty_category(self, name: str) -> bool:
        """
        Check if a category is empty (has no pages or subcategories).

        Args:
            name (str): The name of the category to check

        Returns:
            bool: True if the category is empty, False otherwise
        """
        try:
            if not self.category_exists(name):
                self.logger.debug(f"Category does not exist: {name}")
                return True  # Non-existent categories are considered empty

            category = pywikibot.Category(self.site, name)

            # Check if category has any members
            members = list(category.members())
            is_empty = len(members) == 0

            self.logger.debug(f"Category '{name}' is empty: {is_empty}")
            return is_empty
        except Exception as e:
            error_msg = f"Error checking if category '{name}' is empty: {e}"
            self.logger.error(error_msg)
            return True  # Default to empty on error for safety