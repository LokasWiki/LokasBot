"""
Use case for archiving completed photo requests.

This module handles the main workflow of removing completed requests
from the main page and adding them to the appropriate archive.
"""

import logging
from typing import List, Tuple

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class ArchiveCompletedRequests:
    """
    Use case for archiving completed photo requests.
    
    This class orchestrates the archiving process:
    1. Removes the request template from the main page
    2. Creates an archive entry
    3. Adds the entry to the appropriate archive page
    """
    
    # Constants
    MAIN_PAGE_TITLE = "ويكيبيديا:ورشة الصور/طلبات"
    
    def __init__(self, wiki_repository: WikiRepository):
        """
        Initialize the use case.
        
        Args:
            wiki_repository: Repository for wiki operations
        """
        self.wiki_repository = wiki_repository
        self.logger = logging.getLogger(__name__)
    
    def execute(self, requests: List[PhotoRequest], archive_page: ArchivePage) -> dict:
        """
        Execute the archiving process for completed requests.
        
        All archivable requests are added to the archive page and saved in ONE edit.
        
        Args:
            requests: List of PhotoRequest entities (only archivable ones will be processed)
            archive_page: The archive page to add entries to
            
        Returns:
            Dictionary with results:
            {
                'archived': List of successfully archived request page names,
                'failed': List of failed request page names,
                'skipped': List of skipped (not ready) request page names
            }
        """
        self.logger.info(f"Starting archiving process for {len(requests)} requests")
        
        results = {
            'archived': [],
            'failed': [],
            'skipped': []
        }
        
        # Get the current main page content
        try:
            main_content = self.wiki_repository.get_main_requests_page_content()
        except Exception as e:
            self.logger.error(f"Failed to get main page content: {str(e)}")
            results['failed'] = [r.page_name for r in requests]
            return results
        
        # Collect all archivable requests first
        archivable_requests = []
        for request in requests:
            if request.is_ready_for_archive():
                archivable_requests.append(request)
            else:
                results['skipped'].append(request.page_name)
        
        if not archivable_requests:
            self.logger.info("No archivable requests found")
            return results
        
        # Add ALL entries to the archive page entity first
        for request in archivable_requests:
            entry = ArchiveEntry(
                page_name=request.page_name,
                template_text=request.template_text
            )
            archive_page.add_entry(entry)
        
        # Save the archive page ONCE with all entries
        try:
            success = self.wiki_repository.update_archive_page(
                archive_page,
                f"أرشفة {len(archivable_requests)} طلبات ورشة صور"
            )
            
            if success:
                for request in archivable_requests:
                    results['archived'].append(request.page_name)
                self.logger.info(f"Successfully archived {len(archivable_requests)} requests to archive {archive_page.page_number}")
            else:
                # If save failed, all requests failed
                for request in archivable_requests:
                    results['failed'].append(request.page_name)
                self.logger.error(f"Failed to save archive page {archive_page.page_number}")
                return results
                
        except Exception as e:
            self.logger.error(f"Error saving archive page: {str(e)}")
            for request in archivable_requests:
                results['failed'].append(request.page_name)
            return results
        
        # Save the updated main page content (remove archived templates)
        try:
            updated_content = self._remove_archived_templates(main_content, archivable_requests)
            
            summary = f"أرشفة {len(archivable_requests)} طلبات ورشة صور"
            self.wiki_repository.update_main_requests_page(updated_content, summary)
            self.logger.info(f"Updated main page after archiving {len(archivable_requests)} requests")
            
        except Exception as e:
            self.logger.error(f"Failed to update main page: {str(e)}")
            # Don't mark as failed since archives were already created
        
        self.logger.info(f"Archiving complete: {len(results['archived'])} archived, "
                        f"{len(results['failed'])} failed, {len(results['skipped'])} skipped")
        
        return results
    
    def _archive_single_request(self, request: PhotoRequest, archive_page: ArchivePage,
                                main_content: str) -> bool:
        """
        Archive a single request.
        
        Args:
            request: The PhotoRequest to archive
            archive_page: The archive page to add to
            main_content: Current main page content (for reference)
            
        Returns:
            True if successful, False otherwise
        """
        # Create archive entry
        entry = ArchiveEntry(
            page_name=request.page_name,
            template_text=request.template_text
        )
        
        # Add the entry to the archive page entity FIRST
        # This ensures the entry is included in the content
        archive_page.add_entry(entry)
        
        # Then save the archive page with the entry
        success = self.wiki_repository.update_archive_page(
            archive_page,
            f"أرشفة طلب: {request.page_name}"
        )
        
        if not success:
            # Remove the entry if save failed
            archive_page.entries.remove(entry)
            return False
        
        return True
    
    def _remove_archived_templates(self, content: str, 
                                   archived_requests: List[PhotoRequest]) -> str:
        """
        Remove archived request templates from the main page content.
        
        Args:
            content: The current page content
            archived_requests: List of requests that were archived
            
        Returns:
            Updated content with archived templates removed
        """
        import wikitextparser as wtp
        
        parsed = wtp.parse(content)
        
        # Get the templates to remove (their full text)
        templates_to_remove = set()
        for request in archived_requests:
            if request.is_ready_for_archive():
                templates_to_remove.add(request.template_text.strip())
        
        # Remove each template from the content
        new_content = content
        for template_text in templates_to_remove:
            # Remove the template text (with surrounding whitespace)
            new_content = new_content.replace(template_text, "")
        
        # Clean up multiple consecutive newlines
        import re
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        
        return new_content.strip()
