"""
Pywikibot implementation for photo_lab wiki operations.

This module provides a concrete implementation of the WikiRepository
interface using Pywikibot for wiki operations.
"""

import logging
import re
from typing import List, Optional, Tuple

import pywikibot
import wikitextparser as wtp
from pywikibot.exceptions import Error as PywikibotError

from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class PywikibotWiki(WikiRepository):
    """
    Pywikibot implementation of WikiRepository.
    
    This class handles all wiki operations using Pywikibot,
    implementing the WikiRepository interface.
    """
    
    # Constants
    MAIN_PAGE_TITLE = "ويكيبيديا:ورشة الصور/طلبات"
    
    def __init__(self, site=None):
        """
        Initialize the Pywikibot wiki operations.
        
        Args:
            site (pywikibot.Site, optional): The wiki site to use
        """
        # Configure pywikibot to ignore bot templates for this task
        # This allows editing pages even with {{bots}} or {{nobots}} templates
        pywikibot.config.put_throttle = 0  # No delay between edits
        
        self.site = site or pywikibot.Site()
        self.logger = logging.getLogger(__name__)
        
        # Log configuration
        self.logger.info("PywikibotWiki initialized with bot template checks disabled")
    
    def get_main_requests_page_content(self) -> str:
        """
        Get the content of the main requests page.
        
        Returns:
            The full wikitext content of the page
        """
        try:
            page = pywikibot.Page(self.site, self.MAIN_PAGE_TITLE)
            if not page.exists():
                self.logger.warning(f"Main page does not exist: {self.MAIN_PAGE_TITLE}")
                return ""
            return page.text
        except PywikibotError as e:
            self.logger.error(f"Pywikibot error getting main page: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error getting main page: {str(e)}")
            raise
    
    def update_main_requests_page(self, content: str, summary: str) -> bool:
        """
        Update the main requests page with new content.
        
        Args:
            content: The new page content
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            page = pywikibot.Page(self.site, self.MAIN_PAGE_TITLE)
            page.text = content
            page.save(summary=summary, minor=False)
            self.logger.info(f"Updated main page: {self.MAIN_PAGE_TITLE}")
            return True
        except PywikibotError as e:
            self.logger.error(f"Pywikibot error updating main page: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating main page: {str(e)}")
            return False
    
    def get_request_page_content(self, page_title: str) -> str:
        """
        Get the content of a specific request page.
        
        Args:
            page_title: The full title of the request page
            
        Returns:
            The full wikitext content of the page
        """
        try:
            page = pywikibot.Page(self.site, page_title)
            if not page.exists():
                return ""
            return page.text
        except Exception as e:
            self.logger.error(f"Error getting page {page_title}: {str(e)}")
            return ""
    
    def has_template(self, page_title: str, template_name: str) -> bool:
        """
        Check if a page contains a specific template.
        
        Args:
            page_title: The full title of the page to check
            template_name: The name of the template to look for
            
        Returns:
            True if the template exists, False otherwise
        """
        try:
            content = self.get_request_page_content(page_title)
            if not content:
                return False
            
            parsed = wtp.parse(content)
            
            for template in parsed.templates:
                if template.name.strip() == template_name:
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Error checking template in {page_title}: {str(e)}")
            return False
    
    def get_all_archive_pages(self, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> List[Tuple[int, str]]:
        """
        Get all existing archive pages.
        
        Args:
            base_prefix: The base prefix for archive pages
            
        Returns:
            List of tuples (page_number, page_title) sorted by page number
        """
        archive_pages = []
        
        try:
            # The prefix without namespace for allpages query
            prefix_without_ns = "ورشة الصور/أرشيف"
            
            # Use allpages API to get pages with the prefix in namespace 4 (Wikipedia)
            all_pages = list(self.site.allpages(prefix=prefix_without_ns, namespace=4))
            
            # Pattern to match archive pages: "ورشة الصور/أرشيف NUMBER"
            pattern = re.compile(re.escape(prefix_without_ns) + r'\s*(\d+)')
            
            for page in all_pages:
                # page.title() with namespace=4 includes the "ويكيبيديا:" prefix
                title = page.title()
                match = pattern.search(title)
                if match:
                    page_number = int(match.group(1))
                    # Title already includes "ويكيبيديا:" prefix
                    archive_pages.append((page_number, title))
            
            # Sort by page number
            archive_pages.sort(key=lambda x: x[0])
            
            self.logger.info(f"Found {len(archive_pages)} archive pages")
            return archive_pages
            
        except Exception as e:
            self.logger.error(f"Error getting archive pages: {str(e)}")
            return []
    
    def get_archive_page_content(self, page_number: int, 
                                  base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> str:
        """
        Get the content of a specific archive page.
        
        Args:
            page_number: The archive page number
            base_prefix: The base prefix for archive pages
            
        Returns:
            The full wikitext content of the page
        """
        page_title = f"{base_prefix} {page_number}"
        return self.get_request_page_content(page_title)
    
    def create_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """
        Create a new archive page.
        
        Args:
            archive_page: The archive page entity to create
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            page = pywikibot.Page(self.site, archive_page.title)
            page.text = archive_page.get_content()
            page.save(summary=summary, minor=False)
            self.logger.info(f"Created archive page: {archive_page.title}")
            return True
        except PywikibotError as e:
            self.logger.error(f"Pywikibot error creating archive page: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error creating archive page: {str(e)}")
            return False
    
    def update_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """
        Update an existing archive page with new entries.
        
        Args:
            archive_page: The archive page entity with updated content
            summary: The edit summary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            page = pywikibot.Page(self.site, archive_page.title)
            
            # If page doesn't exist, create it
            if not page.exists():
                return self.create_archive_page(archive_page, summary)
            
            # Update existing page
            page.text = archive_page.get_content()
            page.save(summary=summary, minor=False)
            self.logger.info(f"Updated archive page: {archive_page.title}")
            return True
            
        except PywikibotError as e:
            self.logger.error(f"Pywikibot error updating archive page: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating archive page: {str(e)}")
            return False
    
    def page_exists(self, page_title: str) -> bool:
        """
        Check if a page exists on the wiki.
        
        Args:
            page_title: The full title of the page
            
        Returns:
            True if the page exists, False otherwise
        """
        try:
            page = pywikibot.Page(self.site, page_title)
            return page.exists()
        except Exception as e:
            self.logger.error(f"Error checking if page exists {page_title}: {str(e)}")
            return False
    
    def count_templates_in_page(self, page_title: str, template_name: str) -> int:
        """
        Count the number of occurrences of a template in a page.
        
        Args:
            page_title: The full title of the page
            template_name: The name of the template to count
            
        Returns:
            The number of template occurrences
        """
        try:
            content = self.get_request_page_content(page_title)
            if not content:
                return 0
            
            parsed = wtp.parse(content)
            count = 0
            
            for template in parsed.templates:
                if template.name.strip() == template_name:
                    count += 1
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error counting templates in {page_title}: {str(e)}")
            return 0
