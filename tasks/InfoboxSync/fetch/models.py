"""Data models for the fetch stage."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PageInfo:
    """Data class for page information."""
    title: str
    exists: bool
    content: Optional[str] = None
    langlinks: Optional[Dict[str, str]] = None
    error: Optional[str] = None


@dataclass
class SyncResult:
    """Data class for synchronization results."""
    arabic: PageInfo
    english: Optional[PageInfo]
    sync_possible: bool
    error: Optional[str] = None