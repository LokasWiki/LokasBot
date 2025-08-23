"""
Data layer package.

This package contains concrete implementations of the repository interfaces
defined in the domain layer. These implementations handle the actual data
access operations using external frameworks like pywikibot.

The data layer is responsible for:
- Implementing repository interfaces
- Handling external API calls
- Managing data persistence
- Error handling and logging
"""

from .wiki_page_repository import WikiPageRepository
from .wiki_category_repository import WikiCategoryRepository

__all__ = ['WikiPageRepository', 'WikiCategoryRepository']