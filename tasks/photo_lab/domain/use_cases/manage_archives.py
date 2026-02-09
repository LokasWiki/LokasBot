"""
Use case for managing archive pages.

This module handles finding the latest archive, creating new archives,
and adding entries to existing archives.
"""

import logging
import re
from typing import Optional, Tuple

from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class ManageArchives:
    """
    Use case for managing archive pages.
    
    This class handles all archive-related operations including finding
    the latest archive, creating new archives, and adding entries.
    """
    
    # Constants
    ARCHIVE_PREFIX = "ويكيبيديا:ورشة الصور/أرشيف"
    MAX_ENTRIES_PER_ARCHIVE = 10
    
    def __init__(self, wiki_repository: WikiRepository):
        """
        Initialize the use case.
        
        Args:
            wiki_repository: Repository for wiki operations
        """
        self.wiki_repository = wiki_repository
        self.logger = logging.getLogger(__name__)
    
    def get_or_create_latest_archive(self) -> ArchivePage:
        """
        Get the latest archive page or create a new one if needed.
        
        This method finds the archive with the highest number and checks
        if it has room for more entries and is not bot-restricted.
        If full or restricted, creates a NEW archive (does not go back to old ones).
        Keeps incrementing until it finds a non-restricted archive number.
        
        Returns:
            The ArchivePage to use for new entries
        """
        self.logger.info("Getting or creating latest archive")
        
        # Get all existing archive pages
        archive_pages = self.wiki_repository.get_all_archive_pages(self.ARCHIVE_PREFIX)
        
        if not archive_pages:
            self.logger.info("No existing archives found, creating archive 1")
            return ArchivePage(page_number=1)
        
        # Get the highest numbered archive
        latest_number, latest_title = archive_pages[-1]
        self.logger.info(f"Found latest archive: {latest_title} (number {latest_number})")
        
        # Check if the latest archive is bot-restricted or full
        # Keep incrementing until we find a usable archive number
        current_number = latest_number
        
        while True:
            current_title = f"{self.ARCHIVE_PREFIX} {current_number}"
            
            # Check if this archive page exists
            if self.wiki_repository.page_exists(current_title):
                # Check if bot-restricted
                if self._is_archive_restricted(current_title):
                    self.logger.warning(f"Archive {current_number} is bot-restricted, trying next")
                    current_number += 1
                    continue
                
                # Check if full
                entry_count = self.wiki_repository.count_templates_in_page(
                    current_title,
                    "طلب ورشة صور"
                )
                self.logger.info(f"Archive {current_number} has {entry_count} entries (max: {self.MAX_ENTRIES_PER_ARCHIVE})")
                
                if entry_count >= self.MAX_ENTRIES_PER_ARCHIVE:
                    self.logger.info(f"Archive {current_number} is full, trying next")
                    current_number += 1
                    continue
                
                # Archive exists, not restricted, and has room - use it
                content = self.wiki_repository.get_archive_page_content(
                    current_number,
                    self.ARCHIVE_PREFIX
                )
                return self._load_archive_page(current_number, content)
            else:
                # Page doesn't exist - we can create it
                self.logger.info(f"Archive {current_number} doesn't exist, will create it")
                return ArchivePage(page_number=current_number)
    
    def _is_archive_restricted(self, page_title: str) -> bool:
        """
        Check if an archive page has bot restrictions.
        
        Args:
            page_title: The title of the archive page
            
        Returns:
            True if the page has {{bots}} or {{nobots}} templates
        """
        try:
            has_bots = self.wiki_repository.has_template(page_title, "bots")
            has_nobots = self.wiki_repository.has_template(page_title, "nobots")
            return has_bots or has_nobots
        except Exception as e:
            self.logger.warning(f"Could not check bot restrictions for {page_title}: {str(e)}")
            return False
    
    def add_entry_to_archive(self, archive_page: ArchivePage, entry: ArchiveEntry) -> bool:
        """
        Add an entry to an archive page.
        
        Args:
            archive_page: The archive page to add to
            entry: The entry to add
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Adding entry for '{entry.page_name}' to archive {archive_page.page_number}")
        
        # Add the entry to the archive page entity
        archive_page.add_entry(entry)
        
        # Determine if this is a new archive or an update
        if self.wiki_repository.page_exists(archive_page.title):
            # Update existing archive
            summary = f"أرشفة طلب: {entry.page_name}"
            return self.wiki_repository.update_archive_page(archive_page, summary)
        else:
            # Create new archive
            summary = f"إنشاء أرشيف {archive_page.page_number} وأرشفة طلب: {entry.page_name}"
            return self.wiki_repository.create_archive_page(archive_page, summary)
    
    def _load_archive_page(self, page_number: int, content: str) -> ArchivePage:
        """
        Load an archive page from its content.
        
        Args:
            page_number: The archive page number
            content: The page content
            
        Returns:
            ArchivePage entity with loaded entries
        """
        import wikitextparser as wtp
        
        archive_page = ArchivePage(page_number=page_number)
        parsed = wtp.parse(content)
        
        # Extract existing entries (request templates)
        for template in parsed.templates:
            if template.name.strip() == "طلب ورشة صور":
                # Extract page name from template
                arguments = template.arguments
                page_name = ""
                
                for arg in arguments:
                    if arg.name.strip() == str(arg.positional):
                        page_name = arg.value.strip()
                        break
                
                if page_name:
                    entry = ArchiveEntry(
                        page_name=page_name,
                        template_text=template.string,
                        archive_page_number=page_number
                    )
                    archive_page.add_entry(entry)
        
        self.logger.info(f"Loaded {archive_page.entry_count} entries from archive {page_number}")
        return archive_page
    
    def find_latest_archive_number(self) -> int:
        """
        Find the highest archive number.
        
        Returns:
            The highest archive number, or 0 if no archives exist
        """
        archive_pages = self.wiki_repository.get_all_archive_pages(self.ARCHIVE_PREFIX)
        
        if not archive_pages:
            return 0
        
        return archive_pages[-1][0]
