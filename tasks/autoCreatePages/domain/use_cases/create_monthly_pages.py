"""
Use case for creating monthly maintenance pages.

This use case encapsulates the business logic for creating monthly
maintenance pages on the wiki, following the Clean Architecture principles.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from tasks.autoCreatePages.domain.repositories.page_repository import (
    PageRepository
)
from tasks.autoCreatePages.domain.entities.page import Page


class CreateMonthlyPages:
    """
    Use case for creating monthly maintenance pages.

    This class contains the business logic for creating monthly pages
    based on configuration templates and current date information.
    """

    def __init__(self, page_repository: PageRepository):
        """
        Initialize the CreateMonthlyPages use case.

        Args:
            page_repository (PageRepository): Repository for page operations
        """
        self.page_repository = page_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, page_configs: List[Dict[str, Any]],
                current_date: datetime) -> Dict[str, Any]:
        """
        Execute the use case to create monthly pages.

        Args:
            page_configs (List[Dict[str, Any]]): List of page configurations
                containing template information
            current_date (datetime): The current date to use for page creation

        Returns:
            Dict[str, Any]: Result containing created pages and statistics
        """
        result = {
            'created_pages': [],
            'skipped_pages': [],
            'errors': [],
            'total_processed': 0
        }

        month_name = self._get_month_name(current_date.month)
        year = current_date.year

        month_year = f"{month_name} {year}"
        self.logger.info(f"Starting monthly page creation for {month_year}")

        for config in page_configs:
            try:
                page_title = self._generate_page_title(
                    config['name_template'],
                    month_name,
                    year
                )

                # Check if page already exists
                if self.page_repository.page_exists(page_title):
                    self.logger.info(f"Page already exists: {page_title}")
                    result['skipped_pages'].append(page_title)
                    continue

                # Create the page
                creation_msg = config.get(
                    'creation_message',
                    "بوت:إنشاء صفحات مطلوبة V2.2.0"
                )
                page = Page(
                    title=page_title,
                    content=config['template'],
                    creation_message=creation_msg
                )

                self.page_repository.create_page(page)
                result['created_pages'].append(page_title)
                self.logger.info(f"Successfully created page: {page_title}")

            except Exception as e:
                config_info = str(config)
                error_msg = (f"Failed to create page from config {config_info}: "
                            f"{str(e)}")
                self.logger.error(error_msg)
                result['errors'].append(error_msg)

            result['total_processed'] += 1

        created_count = len(result['created_pages'])
        skipped_count = len(result['skipped_pages'])
        errors_count = len(result['errors'])

        self.logger.info(
            f"Monthly page creation completed. "
            f"Created: {created_count}, "
            f"Skipped: {skipped_count}, "
            f"Errors: {errors_count}"
        )

        return result

    def _get_month_name(self, month: int) -> str:
        """
        Get the Arabic month name for the given month number.

        Args:
            month (int): Month number (1-12)

        Returns:
            str: Arabic month name

        Raises:
            ValueError: If month is not between 1 and 12
        """
        month_names = {
            1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
            5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }

        if month not in month_names:
            month_range = "Must be between 1 and 12."
            raise ValueError(f"Invalid month: {month}. {month_range}")

        return month_names[month]

    def _generate_page_title(self, template: str, month_name: str,
                            year: int) -> str:
        """
        Generate the actual page title by replacing placeholders.

        Args:
            template (str): Template string with placeholders
            month_name (str): Arabic month name
            year (int): Year number

        Returns:
            str: Generated page title
        """
        title = template.replace("MONTH", month_name)
        return title.replace("YEAR", str(year))