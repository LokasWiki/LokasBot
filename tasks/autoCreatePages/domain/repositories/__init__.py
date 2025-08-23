"""
Domain repositories package.

This package contains the repository interfaces that define the contracts
for data access operations, following the Repository pattern.
"""

from .page_repository import PageRepository
from .category_repository import CategoryRepository

__all__ = ['PageRepository', 'CategoryRepository']