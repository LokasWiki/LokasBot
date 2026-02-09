"""
Use case for extracting pending photo requests from the main page.

This module handles parsing the main requests page and extracting
all photo workshop requests.
"""

import logging
from typing import List
import wikitextparser as wtp

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class ExtractPendingRequests:
    """
    Use case for extracting pending photo requests.
    
    This class reads the main requests page and extracts all
    "طلب ورشة صور" templates along with their page name parameters.
    """
    
    # Constants
    MAIN_PAGE_TITLE = "ويكيبيديا:ورشة الصور/طلبات"
    REQUEST_TEMPLATE_NAME = "طلب ورشة صور"
    
    def __init__(self, wiki_repository: WikiRepository):
        """
        Initialize the use case.
        
        Args:
            wiki_repository: Repository for wiki operations
        """
        self.wiki_repository = wiki_repository
        self.logger = logging.getLogger(__name__)
    
    def execute(self) -> List[PhotoRequest]:
        """
        Execute the use case to extract all pending requests.
        
        Returns:
            List of PhotoRequest entities
            
        Raises:
            Exception: If the page cannot be retrieved or parsed
        """
        self.logger.info(f"Extracting requests from {self.MAIN_PAGE_TITLE}")
        
        try:
            content = self.wiki_repository.get_main_requests_page_content()
            requests = self._parse_requests(content)
            self.logger.info(f"Found {len(requests)} pending requests")
            return requests
            
        except Exception as e:
            self.logger.error(f"Failed to extract requests: {str(e)}")
            raise
    
    def _parse_requests(self, content: str) -> List[PhotoRequest]:
        """
        Parse the page content and extract photo requests.
        
        Args:
            content: The wikitext content of the page
            
        Returns:
            List of PhotoRequest entities
        """
        requests = []
        parsed = wtp.parse(content)
        
        for template in parsed.templates:
            template_name = template.name.strip()
            
            # Check if this is a request template
            if template_name == self.REQUEST_TEMPLATE_NAME:
                request = self._extract_request_from_template(template)
                if request:
                    requests.append(request)
                    self.logger.debug(f"Extracted request for page: {request.page_name}")
        
        return requests
    
    def _extract_request_from_template(self, template) -> PhotoRequest:
        """
        Extract a PhotoRequest from a parsed template.
        
        Args:
            template: The parsed wikitext template
            
        Returns:
            PhotoRequest entity or None if invalid
        """
        try:
            # Get all arguments
            arguments = template.arguments
            
            if not arguments:
                self.logger.warning("Found template with no arguments, skipping")
                return None
            
            # Page name is the first argument
            # In wikitextparser, arguments are accessed directly
            page_name = ""
            
            # Try to get the first argument value
            for arg in arguments:
                # Check if it's a positional argument (unnamed)
                if hasattr(arg, 'positional') and arg.positional is not None:
                    if arg.positional == 1:  # First positional argument
                        page_name = str(arg.value).strip()
                        break
                # Fallback: try name attribute
                elif hasattr(arg, 'name'):
                    name_str = str(arg.name).strip()
                    # If name is numeric and equals 1, it's the first positional arg
                    if name_str == '1' or name_str == '':
                        page_name = str(arg.value).strip()
                        break
            
            # If still no page name, try the first argument's value directly
            if not page_name and arguments:
                try:
                    page_name = str(arguments[0].value).strip()
                except:
                    pass
            
            if not page_name:
                self.logger.warning("Could not extract page name from template")
                return None
            
            # Get the full template text
            template_text = template.string
            
            return PhotoRequest(
                page_name=page_name,
                template_text=template_text
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting request from template: {str(e)}")
            return None
