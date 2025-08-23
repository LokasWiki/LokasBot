"""
Repository interface for Wiki Category operations.

This interface defines the contract for category data access operations,
following the Repository pattern to abstract data access from business logic.
"""

from abc import ABC, abstractmethod
from typing import Optional
from tasks.autoCreatePages.domain.entities.category import Category


class CategoryRepository(ABC):
    """
    Abstract repository interface for wiki category operations.

    This interface defines the contract for data access operations
    related to wiki categories, allowing for different implementations
    (e.g., Wiki API, mock, test implementations).
    """

    @abstractmethod
    def category_exists(self, name: str) -> bool:
        """
        Check if a category with the given name exists.

        Args:
            name (str): The name of the category to check

        Returns:
            bool: True if the category exists, False otherwise
        """
        pass

    @abstractmethod
    def create_category(self, category: Category) -> None:
        """
        Create a new wiki category.

        Args:
            category (Category): The category entity to create

        Raises:
            Exception: If the category creation fails
        """
        pass

    @abstractmethod
    def get_category_content(self, name: str) -> Optional[str]:
        """
        Get the content of an existing category.

        Args:
            name (str): The name of the category

        Returns:
            Optional[str]: The category content if it exists, None otherwise
        """
        pass

    @abstractmethod
    def update_category(self, category: Category) -> None:
        """
        Update an existing wiki category.

        Args:
            category (Category): The category entity with updated content

        Raises:
            Exception: If the category update fails or category doesn't exist
        """
        pass

    @abstractmethod
    def is_empty_category(self, name: str) -> bool:
        """
        Check if a category is empty (has no pages or subcategories).

        Args:
            name (str): The name of the category to check

        Returns:
            bool: True if the category is empty, False otherwise
        """
        pass