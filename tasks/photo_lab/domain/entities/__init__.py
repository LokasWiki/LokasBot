"""
Domain entities for the photo_lab task.

This package contains the core business entities for the photo workshop
task, following Domain-Driven Design principles.
"""

from .photo_request import PhotoRequest
from .archive_entry import ArchiveEntry, ArchivePage

__all__ = ['PhotoRequest', 'ArchiveEntry', 'ArchivePage']
