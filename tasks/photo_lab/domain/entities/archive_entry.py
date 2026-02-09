"""
Domain entity representing an archive entry.

This entity represents a request that has been archived, containing
the archived template and metadata.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ArchiveEntry:
    """
    Entity representing an archived photo request.
    
    Attributes:
        page_name: The name of the page that was requested
        template_text: The full template text archived
        archived_at: Timestamp when the request was archived
        archive_page_number: The archive page number where this entry is stored
    """
    page_name: str
    template_text: str
    archived_at: Optional[datetime] = None
    archive_page_number: int = 0
    
    def __post_init__(self):
        """Initialize default timestamp if not provided."""
        if self.archived_at is None:
            self.archived_at = datetime.now()
    
    def __str__(self) -> str:
        """String representation of the archive entry."""
        return f"ArchiveEntry(page='{self.page_name}', archive={self.archive_page_number})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"ArchiveEntry(page_name='{self.page_name}', "
                f"template_text='{self.template_text[:50]}...', "
                f"archived_at={self.archived_at}, "
                f"archive_page_number={self.archive_page_number})")
    
    def get_archive_page_title(self, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> str:
        """
        Get the full archive page title.
        
        Args:
            base_prefix: The base prefix for archive pages
            
        Returns:
            The full title of the archive page
        """
        return f"{base_prefix} {self.archive_page_number}"
    
    def format_for_archive(self) -> str:
        """
        Format the entry for inclusion in an archive page.
        
        Returns:
            Formatted text ready to be added to archive
        """
        return f"\n{self.template_text.strip()}\n"


@dataclass
class ArchivePage:
    """
    Entity representing an archive page.
    
    Attributes:
        page_number: The archive page number
        entries: List of archive entries in this page
        base_prefix: The base prefix for archive pages
    """
    page_number: int
    entries: list = None
    base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف"
    
    def __post_init__(self):
        """Initialize entries list if not provided."""
        if self.entries is None:
            self.entries = []
    
    @property
    def title(self) -> str:
        """Get the full title of the archive page."""
        return f"{self.base_prefix} {self.page_number}"
    
    @property
    def entry_count(self) -> int:
        """Get the number of entries in this archive."""
        return len(self.entries)
    
    def is_full(self, max_entries: int = 10) -> bool:
        """
        Check if the archive page is full.
        
        Args:
            max_entries: Maximum number of entries allowed (default: 10)
            
        Returns:
            True if archive is full, False otherwise
        """
        return self.entry_count >= max_entries
    
    def add_entry(self, entry: ArchiveEntry) -> None:
        """
        Add an entry to this archive page.
        
        Args:
            entry: The archive entry to add
        """
        entry.archive_page_number = self.page_number
        self.entries.append(entry)
    
    def get_header(self) -> str:
        """
        Get the standard archive page header.
        
        Returns:
            The formatted header text
        """
        return f"""
{{{{تصفح أرشيف|{self.page_number}}}}}
{{{{تمت الأرشفة}}}}

"""
    
    def get_content(self) -> str:
        """
        Get the full content of the archive page.
        
        Returns:
            The complete page content including header and all entries
        """
        content = self.get_header()
        for entry in self.entries:
            content += entry.format_for_archive()
        return content.strip()
