"""
Presentation layer for wiki operations.

This module provides a presentation layer that abstracts the details
of wiki operations and provides a clean interface for the use cases.
It follows the Clean Architecture principle of separating infrastructure
concerns from business logic.
"""

import logging
import pywikibot


class WikiOperations:
    """
    Presentation layer for wiki operations.

    This class provides high-level operations for interacting with the wiki,
    abstracting away the details of the pywikibot library and providing
    a clean interface for the domain layer.
    """

    def __init__(self, site_name: str = "ar"):
        """
        Initialize the WikiOperations with a specific wiki site.

        Args:
            site_name (str): The name of the wiki site
                (default: "ar" for Arabic)
        """
        self.site_name = site_name
        self.site = pywikibot.Site(site_name)
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Initialized WikiOperations for site: {site_name}")

    def get_site(self) -> pywikibot.Site:
        """
        Get the pywikibot site object.

        Returns:
            pywikibot.Site: The site object for wiki operations
        """
        return self.site

    def validate_date(self, day: int, month: int, year: int) -> bool:
        """
        Validate if the given date components form a valid date.

        Args:
            day (int): Day of the month (1-31)
            month (int): Month of the year (1-12)
            year (int): Year

        Returns:
            bool: True if the date is valid, False otherwise
        """
        try:
            # Try to create a date object to validate
            import datetime
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False

    def get_current_date_info(self) -> dict:
        """
        Get information about the current date.

        Returns:
            dict: Dictionary containing current date information including
                  day, month, year, and formatted month name
        """
        import datetime
        now = datetime.datetime.now()

        # Get Arabic month name
        month_names = {
            1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
            5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }

        return {
            'day': now.day,
            'month': now.month,
            'year': now.year,
            'month_name': month_names.get(now.month, ''),
            'datetime': now
        }

    def is_first_day_of_month(self) -> bool:
        """
        Check if today is the first day of the month.

        Returns:
            bool: True if today is the 1st day of the month, False otherwise
        """
        date_info = self.get_current_date_info()
        return date_info['day'] == 1

    def format_timestamp(self, timestamp_str: str) -> str:
        """
        Format a timestamp string into a readable format.

        This is a placeholder for the DateFormatter functionality.
        In a real implementation, this would use the DateFormatter
        from the check_usernames module.

        Args:
            timestamp_str (str): Timestamp string (e.g., "20231201120000")

        Returns:
            str: Formatted timestamp string
        """
        # For now, return the timestamp as-is
        # In production, this would use DateFormatter("ar").format_timestamp()
        return timestamp_str

    def log_operation(self, operation: str, details: str,
                      success: bool = True) -> None:
        """
        Log a wiki operation with appropriate level.

        Args:
            operation (str): The operation being performed
            details (str): Details about the operation
            success (bool): Whether the operation was successful
        """
        if success:
            self.logger.info(f"Wiki operation '{operation}': {details}")
        else:
            error_msg = f"Wiki operation '{operation}' failed: {details}"
            self.logger.error(error_msg)

    def get_default_creation_message(self, operation_type: str) -> str:
        """
        Get a default creation message for different operation types.

        Args:
            operation_type (str): Type of operation (page, category, etc.)

        Returns:
            str: Default creation message
        """
        messages = {
            'page': "بوت:إنشاء صفحات مطلوبة V2.2.0",
            'category': "بوت:إنشاء صفحات مطلوبة V1.2.0",
            'default': "بوت:إنشاء صفحات مطلوبة"
        }

        return messages.get(operation_type, messages['default'])