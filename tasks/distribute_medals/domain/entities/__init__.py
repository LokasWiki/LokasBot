"""
Domain entities for medal distribution system.

This module contains the core business entities that represent
the fundamental data structures of the medal distribution domain.
"""

from .medal import Medal
from .user import User
from .template import Template
from .signature import Signature

__all__ = ["Medal", "User", "Template", "Signature"]