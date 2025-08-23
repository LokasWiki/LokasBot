"""
Use case for creating block user categories.

This use case encapsulates the business logic for creating categories
for usernames that are candidates for blocking, following the Clean Architecture principles.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from tasks.autoCreatePages.domain.repositories.category_repository import (
    CategoryRepository
)
from tasks.autoCreatePages.domain.entities.category import Category


class CreateBlockCategory:
    """
    Use case for creating block user categories.

    This class contains the business logic for creating categories
    for usernames that are candidates for blocking.
    """

    def __init__(self, category_repository: CategoryRepository):
        """
        Initialize the CreateBlockCategory use case.

        Args:
            category_repository (CategoryRepository): Repository for category
                operations
        """
        self.category_repository = category_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, category_config: Dict[str, Any],
                current_date: datetime) -> Dict[str, Any]:
        """
        Execute the use case to create a block category.

        Args:
            category_config (Dict[str, Any]): Category configuration containing
                template and naming information
            current_date (datetime): The current date to use for category creation

        Returns:
            Dict[str, Any]: Result containing creation status and category info
        """
        result = {
            'created': False,
            'category_name': None,
            'error': None,
            'action_taken': None
        }

        try:
            # Generate category name with Arabic date format
            category_name = self._generate_category_name(
                category_config['name_template'],
                current_date
            )

            result['category_name'] = category_name

            # Check if category already exists
            if self.category_repository.category_exists(category_name):
                self.logger.info(f"Category already exists: {category_name}")

                # Check if it's empty and needs content
                if self.category_repository.is_empty_category(category_name):
                    # Add template content to existing empty category
                    category = Category(
                        name=category_name,
                        template=category_config['template'],
                        creation_message=category_config.get(
                            'creation_message',
                            "بوت:إنشاء صفحات مطلوبة V1.2.0"
                        )
                    )

                    self.category_repository.update_category(category)
                    result['created'] = True
                    result['action_taken'] = 'updated'
                    self.logger.info(f"Updated empty category: {category_name}")
                else:
                    result['action_taken'] = 'skipped'
                    self.logger.info(f"Category not empty, skipping: {category_name}")
            else:
                # Create new category
                category = Category(
                    name=category_name,
                    template=category_config['template'],
                    creation_message=category_config.get(
                        'creation_message',
                        "بوت:إنشاء صفحات مطلوبة V1.2.0"
                    )
                )

                self.category_repository.create_category(category)
                result['created'] = True
                result['action_taken'] = 'created'
                self.logger.info(f"Successfully created category: {category_name}")

        except Exception as e:
            error_msg = f"Failed to create/update category: {e}"
            self.logger.error(error_msg)
            result['error'] = error_msg

        return result

    def _generate_category_name(self, template: str,
                               current_date: datetime) -> str:
        """
        Generate the category name with Arabic date format.

        Args:
            template (str): Template string for category name
            current_date (datetime): Current date for formatting

        Returns:
            str: Generated category name with Arabic date
        """
        # Get Arabic month name
        month_names = {
            1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
            5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }

        month_name = month_names.get(current_date.month, '')
        day = current_date.day
        year = current_date.year

        # Format as "DD MonthName YYYY" in Arabic
        arabic_date = f"{day} {month_name} {year}"

        return template.replace("DATE_PLACEHOLDER", arabic_date)