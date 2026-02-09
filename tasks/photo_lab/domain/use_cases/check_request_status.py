"""
Use case for checking the status of photo requests.

This module handles checking if a request page has the "منظور" template,
which indicates the request is ready for archiving.
"""

import logging
from typing import List

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class CheckRequestStatus:
    """
    Use case for checking request statuses.
    
    This class checks each photo request page to see if it contains
    the "منظور" template, marking it as ready for archiving.
    """
    
    # Constants
    PERSPECTIVE_TEMPLATE = "منظور"
    
    def __init__(self, wiki_repository: WikiRepository):
        """
        Initialize the use case.
        
        Args:
            wiki_repository: Repository for wiki operations
        """
        self.wiki_repository = wiki_repository
        self.logger = logging.getLogger(__name__)
    
    def execute(self, requests: List[PhotoRequest]) -> List[PhotoRequest]:
        """
        Check the status of all requests and mark those ready for archiving.
        
        Args:
            requests: List of PhotoRequest entities to check
            
        Returns:
            The same list with has_perspective updated
        """
        self.logger.info(f"Checking status of {len(requests)} requests")
        
        for request in requests:
            try:
                has_perspective = self._check_request(request)
                if has_perspective:
                    request.mark_as_archivable()
                    self.logger.info(f"Request '{request.page_name}' has perspective template, ready for archive")
                else:
                    self.logger.debug(f"Request '{request.page_name}' does not have perspective template")
                    
            except Exception as e:
                self.logger.error(f"Failed to check request '{request.page_name}': {str(e)}")
                # Continue with other requests even if one fails
                continue
        
        ready_count = sum(1 for r in requests if r.is_ready_for_archive())
        self.logger.info(f"Found {ready_count} requests ready for archiving")
        
        return requests
    
    def _check_request(self, request: PhotoRequest) -> bool:
        """
        Check if a single request has the perspective template.
        
        Args:
            request: The PhotoRequest to check
            
        Returns:
            True if the request page has the منظور template
        """
        self.logger.debug(f"Checking request page: {request.request_page_title}")
        
        # Check if the request page exists
        if not self.wiki_repository.page_exists(request.request_page_title):
            self.logger.warning(f"Request page does not exist: {request.request_page_title}")
            return False
        
        # Check for the perspective template
        has_perspective = self.wiki_repository.has_template(
            request.request_page_title,
            self.PERSPECTIVE_TEMPLATE
        )
        
        return has_perspective
    
    def get_archivable_requests(self, requests: List[PhotoRequest]) -> List[PhotoRequest]:
        """
        Filter and return only requests that are ready for archiving.
        
        Args:
            requests: List of PhotoRequest entities
            
        Returns:
            List of requests that have the perspective template
        """
        return [r for r in requests if r.is_ready_for_archive()]
