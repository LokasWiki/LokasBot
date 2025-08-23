"""
Infrastructure layer for the CI/CD Log Task.

This package contains all the infrastructure implementations
that handle external dependencies and data access.
"""

from .github_api import GitHubAPI
from .wiki_operations import WikiOperations

__all__ = ['GitHubAPI', 'WikiOperations']