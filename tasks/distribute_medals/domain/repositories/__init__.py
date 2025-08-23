"""
Domain repository interfaces for medal distribution system.

This module contains abstract repository interfaces that define
the contracts for data access operations, following the Repository pattern.
"""

from .database_repository import DatabaseRepository
from .wiki_repository import WikiRepository
from .signature_repository import SignatureRepository

__all__ = ["DatabaseRepository", "WikiRepository", "SignatureRepository"]