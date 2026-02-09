"""
Controller for the photo_lab task.

This module orchestrates the entire photo lab archiving workflow,
coordinating between the different use cases.
"""

import logging
from typing import Dict, List

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.entities.archive_entry import ArchivePage
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository
from tasks.photo_lab.domain.use_cases.extract_pending_requests import ExtractPendingRequests
from tasks.photo_lab.domain.use_cases.check_request_status import CheckRequestStatus
from tasks.photo_lab.domain.use_cases.manage_archives import ManageArchives
from tasks.photo_lab.domain.use_cases.archive_completed_requests import ArchiveCompletedRequests


class PhotoLabController:
    """
    Controller for the photo lab archiving workflow.
    
    This class coordinates the entire process:
    1. Extract pending requests from the main page
    2. Check which requests have the perspective template
    3. Get or create the appropriate archive page
    4. Archive completed requests
    """
    
    def __init__(self, wiki_repository: WikiRepository):
        """
        Initialize the controller.
        
        Args:
            wiki_repository: Repository for wiki operations
        """
        self.wiki_repository = wiki_repository
        self.logger = logging.getLogger(__name__)
        
        # Initialize use cases
        self.extract_use_case = ExtractPendingRequests(wiki_repository)
        self.check_status_use_case = CheckRequestStatus(wiki_repository)
        self.manage_archives_use_case = ManageArchives(wiki_repository)
        self.archive_use_case = ArchiveCompletedRequests(wiki_repository)
    
    def run(self) -> Dict:
        """
        Run the complete photo lab archiving workflow.
        
        Returns:
            Dictionary with results of the operation:
            {
                'success': bool,
                'total_requests': int,
                'archivable_requests': int,
                'archived': List[str],
                'failed': List[str],
                'skipped': List[str],
                'archive_page_number': int,
                'errors': List[str]
            }
        """
        self.logger.info("=== Starting Photo Lab Archiving Workflow ===")
        
        results = {
            'success': False,
            'total_requests': 0,
            'archivable_requests': 0,
            'archived': [],
            'failed': [],
            'skipped': [],
            'archive_page_number': 0,
            'errors': []
        }
        
        try:
            # Step 1: Extract pending requests
            self.logger.info("Step 1: Extracting pending requests...")
            requests = self.extract_use_case.execute()
            results['total_requests'] = len(requests)
            
            if not requests:
                self.logger.info("No pending requests found")
                results['success'] = True
                return results
            
            self.logger.info(f"Found {len(requests)} pending requests")
            
            # Step 2: Check request statuses
            self.logger.info("Step 2: Checking request statuses...")
            requests = self.check_status_use_case.execute(requests)
            
            archivable_requests = self.check_status_use_case.get_archivable_requests(requests)
            results['archivable_requests'] = len(archivable_requests)
            
            if not archivable_requests:
                self.logger.info("No requests ready for archiving")
                results['success'] = True
                return results
            
            self.logger.info(f"Found {len(archivable_requests)} requests ready for archiving")
            
            # Step 3: Get or create archive page
            self.logger.info("Step 3: Getting or creating archive page...")
            archive_page = self.manage_archives_use_case.get_or_create_latest_archive()
            results['archive_page_number'] = archive_page.page_number
            
            self.logger.info(f"Using archive page: {archive_page.title}")
            
            # Step 4: Archive completed requests
            self.logger.info("Step 4: Archiving completed requests...")
            archive_results = self.archive_use_case.execute(archivable_requests, archive_page)
            
            results['archived'] = archive_results['archived']
            results['failed'] = archive_results['failed']
            results['skipped'] = archive_results['skipped']
            
            # Determine success
            results['success'] = len(results['archived']) > 0 and len(results['failed']) == 0
            
            self.logger.info("=== Photo Lab Archiving Workflow Complete ===")
            self.logger.info(f"Archived: {len(results['archived'])}, Failed: {len(results['failed'])}, Skipped: {len(results['skipped'])}")
            
        except Exception as e:
            error_msg = f"Workflow failed: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
            results['success'] = False
        
        return results
    
    def run_dry_mode(self) -> Dict:
        """
        Run the workflow in dry mode (no actual changes).
        
        This mode is useful for testing and verifying what would be archived
        without making any actual changes to the wiki.
        
        Returns:
            Dictionary with results of the dry run
        """
        self.logger.info("=== Starting Photo Lab Archiving Workflow (DRY MODE) ===")
        
        results = {
            'success': True,
            'total_requests': 0,
            'archivable_requests': 0,
            'archived': [],
            'would_archive': [],
            'errors': []
        }
        
        try:
            # Step 1: Extract pending requests
            requests = self.extract_use_case.execute()
            results['total_requests'] = len(requests)
            
            if not requests:
                self.logger.info("No pending requests found")
                return results
            
            # Step 2: Check request statuses
            requests = self.check_status_use_case.execute(requests)
            archivable_requests = self.check_status_use_case.get_archivable_requests(requests)
            results['archivable_requests'] = len(archivable_requests)
            
            # Just report what would be archived
            for request in archivable_requests:
                results['would_archive'].append(request.page_name)
                self.logger.info(f"Would archive: {request.page_name}")
            
            self.logger.info(f"\nSummary: Would archive {len(results['would_archive'])} requests")
            
        except Exception as e:
            error_msg = f"Dry run failed: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
            results['success'] = False
        
        return results
