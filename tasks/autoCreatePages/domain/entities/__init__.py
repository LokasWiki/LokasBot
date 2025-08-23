"""
Domain entities package.

This package contains the core business entities for the autoCreatePages
task, following Domain-Driven Design principles.
"""

from .page import Page
from .category import Category

__all__ = ['Page', 'Category']