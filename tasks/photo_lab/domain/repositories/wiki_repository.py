"""
Repository interface for Wiki operations.

This module defines the abstract interface for all wiki-related operations,
allowing for different implementations (e.g., pywikibot, mock implementations).
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage


class WikiRepository(ABC):
    """
    Abstract interface for wiki operations.
    
    This interface defines all wiki-related operations needed by the photo_lab task.
    Implementations should handle the actual wiki interactions (e.g., using pywikibot).
    """
    
    @abstractmethod
    def get_main_requests_page_content(self) -> str:
        """
        Get the content of the main requests page.
        
        Returns:
            The full wikitext content of the page
            
        Raises:
            Exception: If the page cannot be retrieved
        """
        pass
    
    @abstractmethod
    def update_main_requests_page(self, content: str, summary: str) -> bool:
        """
        Update the main requests page with new content.
        
        Args:
            content: The new page content
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_request_page_content(self, page_title: str) -> str:
        """
        Get the content of a specific request page.
        
        Args:
            page_title: The full title of the request page
            
        Returns:
            The full wikitext content of the page
        """
        pass
    
    @abstractmethod
    def has_template(self, page_title: str, template_name: str) -> bool:
        """
        Check if a page contains a specific template.
        
        Args:
            page_title: The full title of the page to check
            template_name: The name of the template to look for
            
        Returns:
            True if the template exists, False otherwise
        """
        pass
    
    @abstractmethod
    def get_all_archive_pages(self, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> List[Tuple[int, str]]:
        """
        Get all existing archive pages.
        
        Args:
            base_prefix: The base prefix for archive pages
            
        Returns:
            List of tuples (page_number, page_title) sorted by page number
        """
        pass
    
    @abstractmethod
    def get_archive_page_content(self, page_number: int, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> str:
        """
        Get the content of a specific archive page.
        
        Args:
            page_number: The archive page number
            base_prefix: The base prefix for archive pages
            
        Returns:
            The full wikitext content of the page
        """
        pass
    
    @abstractmethod
    def create_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """
        Create a new archive page.
        
        Args:
            archive_page: The archive page entity to create
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def update_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """
        Update an existing archive page with new entries.
        
        Args:
            archive_page: The archive page entity with updated content
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def page_exists(self, page_title: str) -> bool:
        """
        Check if a page exists on the wiki.
        
        Args:
            page_title: The full title of the page
            
        Returns:
            True if the page exists, False otherwise
        """
        pass
    
    @abstractmethod
    def count_templates_in_page(self, page_title: str, template_name: str) -> int:
        """
        Count the number of occurrences of a template in a page.
        
        Args:
            page_title: The full title of the page
            template_name: The name of the template to count
            
        Returns:
            The number of template occurrences
        """
        pass
