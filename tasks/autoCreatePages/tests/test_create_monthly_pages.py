"""
Unit tests for the CreateMonthlyPages use case.

This module demonstrates the testability benefits of the Clean Architecture
approach by providing isolated unit tests for the business logic.
"""

import unittest
from datetime import datetime
from unittest.mock import Mock

from tasks.autoCreatePages.domain.use_cases.create_monthly_pages import (
    CreateMonthlyPages
)
from tasks.autoCreatePages.domain.repositories.page_repository import (
    PageRepository
)
from tasks.autoCreatePages.domain.entities.page import Page


class TestCreateMonthlyPages(unittest.TestCase):
    """Test cases for CreateMonthlyPages use case."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_page_repository = Mock(spec=PageRepository)
        self.use_case = CreateMonthlyPages(self.mock_page_repository)

    def test_execute_creates_pages_successfully(self):
        """Test successful page creation."""
        # Arrange
        test_date = datetime(2024, 1, 15)  # January 2024
        page_configs = [
            {
                "name_template": "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR",
                "template": "{{تصنيف تهذيب شهري}}",
                "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
            }
        ]

        # Mock repository behavior
        self.mock_page_repository.page_exists.return_value = False
        self.mock_page_repository.create_page.return_value = None

        # Act
        result = self.use_case.execute(page_configs, test_date)

        # Assert
        self.assertEqual(len(result['created_pages']), 1)
        self.assertEqual(len(result['skipped_pages']), 0)
        self.assertEqual(len(result['errors']), 0)
        self.assertEqual(result['total_processed'], 1)

        # Verify repository was called correctly
        self.mock_page_repository.page_exists.assert_called_once()
        self.mock_page_repository.create_page.assert_called_once()

        # Verify the page was created with correct data
        created_page = self.mock_page_repository.create_page.call_args[0][0]
        self.assertIsInstance(created_page, Page)
        self.assertIn("يناير", created_page.title)  # Arabic January
        self.assertEqual(created_page.content, "{{تصنيف تهذيب شهري}}")

    def test_execute_skips_existing_pages(self):
        """Test that existing pages are skipped."""
        # Arrange
        test_date = datetime(2024, 1, 15)
        page_configs = [
            {
                "name_template": "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR",
                "template": "{{تصنيف تهذيب شهري}}",
                "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
            }
        ]

        # Mock repository behavior - page exists
        self.mock_page_repository.page_exists.return_value = True

        # Act
        result = self.use_case.execute(page_configs, test_date)

        # Assert
        self.assertEqual(len(result['created_pages']), 0)
        self.assertEqual(len(result['skipped_pages']), 1)
        self.assertEqual(len(result['errors']), 0)

        # Verify create_page was not called
        self.mock_page_repository.create_page.assert_not_called()

    def test_get_month_name_valid_months(self):
        """Test month name conversion for all valid months."""
        month_names = {
            1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل",
            5: "مايو", 6: "يونيو", 7: "يوليو", 8: "أغسطس",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }

        for month_num, expected_name in month_names.items():
            with self.subTest(month=month_num):
                result = self.use_case._get_month_name(month_num)
                self.assertEqual(result, expected_name)

    def test_get_month_name_invalid_month(self):
        """Test month name conversion for invalid month."""
        with self.assertRaises(ValueError) as context:
            self.use_case._get_month_name(13)

        self.assertIn("Invalid month: 13", str(context.exception))
        self.assertIn("Must be between 1 and 12", str(context.exception))

    def test_generate_page_title_replaces_placeholders(self):
        """Test page title generation with placeholder replacement."""
        template = "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR"
        month_name = "يناير"
        year = 2024

        result = self.use_case._generate_page_title(template, month_name, year)

        expected = "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ يناير 2024"
        self.assertEqual(result, expected)

    def test_execute_handles_repository_errors(self):
        """Test error handling when repository operations fail."""
        # Arrange
        test_date = datetime(2024, 1, 15)
        page_configs = [
            {
                "name_template": "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR",
                "template": "{{تصنيف تهذيب شهري}}",
                "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
            }
        ]

        # Mock repository to raise an exception
        self.mock_page_repository.page_exists.return_value = False
        self.mock_page_repository.create_page.side_effect = Exception("Wiki API Error")

        # Act
        result = self.use_case.execute(page_configs, test_date)

        # Assert
        self.assertEqual(len(result['created_pages']), 0)
        self.assertEqual(len(result['skipped_pages']), 0)
        self.assertEqual(len(result['errors']), 1)
        self.assertIn("Wiki API Error", result['errors'][0])


if __name__ == '__main__':
    unittest.main()