"""Domain entity representing the outcome of archiving a single page."""

from dataclasses import dataclass


@dataclass
class ArchiveResult:
    """Result of archiving one discussion page.

    Attributes:
        page_title: The talk page that was processed.
        status: One of ``archived``, ``skipped``, ``failed`` or ``dry_run``.
        reason: Human-readable reason for skipped/failed results.
        archived_count: Number of sections moved to the archive.
        kept_count: Number of sections left on the page.
        archive_title: Title of the archive page that received the sections.
        new_counter: The archive counter after the operation.
        new_page_text: The page text that was (or would be) written.
        new_archive_text: The archive text that was (or would be) written.
    """

    page_title: str
    status: str = "skipped"
    reason: str = ""
    archived_count: int = 0
    kept_count: int = 0
    archive_title: str = ""
    new_counter: int = 0
    new_page_text: str = ""
    new_archive_text: str = ""
