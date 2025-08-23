"""
Wiki infrastructure implementations.

This module contains concrete implementations for wiki operations
using various wiki APIs like Pywikibot, MediaWiki API, etc.
"""

from .pywikibot_wiki import PywikibotWiki

__all__ = ["PywikibotWiki"]