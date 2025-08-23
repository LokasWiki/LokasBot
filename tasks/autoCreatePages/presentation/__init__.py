"""
Presentation layer package.

This package contains the presentation layer components that handle
the interaction with external frameworks and provide interfaces
for the use cases to interact with infrastructure concerns.

The presentation layer is responsible for:
- Handling external API interactions (pywikibot)
- Managing framework-specific operations
- Providing clean interfaces for infrastructure access
- Abstracting external dependencies
"""

from .wiki_operations import WikiOperations

__all__ = ['WikiOperations']