"""
Domain repositories for the CI/CD Log Task.

This package contains all the repository interfaces that define
the contracts for data access operations.
"""

from .github_repository import GitHubRepository
from .wiki_repository import WikiRepository

__all__ = ['GitHubRepository', 'WikiRepository']