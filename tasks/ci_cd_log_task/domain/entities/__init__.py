"""
Domain entities for the CI/CD Log Task.

This package contains all the domain entities that represent
the core business data structures.
"""

from .commit_info import CommitInfo
from .bot_log import BotLog

__all__ = ['CommitInfo', 'BotLog']