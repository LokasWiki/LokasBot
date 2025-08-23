"""
Unit tests for the CreateBlockCategory use case.

This module tests the block category creation functionality,
including the Arabic date formatting.
"""

import unittest
from datetime import datetime
from unittest.mock import Mock

from tasks.autoCreatePages.domain.use_cases.create_block_category import (
    CreateBlockCategory
)
from tasks.autoCreatePages.domain.repositories.category_repository import (
    CategoryRepository
)
from tasks.autoCreatePages.domain.entities.category import Category


class TestCreateBlockCategory(unittest.TestCase):
    """Test cases for CreateBlockCategory use case."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.use_case = CreateBlockCategory(self.mock_category_repository)

    def test_generate_category_name_arabic_format(self):
        """Test category name generation with Arabic date format."""
        template = "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER"
        test_date = datetime(2025, 3, 27)  # March 27, 2025

        result = self.use_case._generate_category_name(template, test_date)

        expected = "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ 27 مارس 2025"
        self.assertEqual(result, expected)

    def test_generate_category_name_different_months(self):
        """Test category name generation for different Arabic months."""
        template = "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER"

        test_cases = [
            (datetime(2025, 1, 15), "15 يناير 2025"),
            (datetime(2025, 2, 20), "20 فبراير 2025"),
            (datetime(2025, 3, 10), "10 مارس 2025"),
            (datetime(2025, 4, 5), "5 أبريل 2025"),
            (datetime(2025, 5, 12), "12 مايو 2025"),
            (datetime(2025, 6, 8), "8 يونيو 2025"),
            (datetime(2025, 7, 25), "25 يوليو 2025"),
            (datetime(2025, 8, 30), "30 أغسطس 2025"),
            (datetime(2025, 9, 18), "18 سبتمبر 2025"),
            (datetime(2025, 10, 22), "22 أكتوبر 2025"),
            (datetime(2025, 11, 14), "14 نوفمبر 2025"),
            (datetime(2025, 12, 31), "31 ديسمبر 2025"),
        ]

        for test_date, expected_date in test_cases:
            with self.subTest(month=test_date.month):
                result = self.use_case._generate_category_name(template, test_date)
                expected = f"تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ {expected_date}"
                self.assertEqual(result, expected)

    def test_execute_creates_category_successfully(self):
        """Test successful category creation."""
        test_date = datetime(2025, 3, 27)
        category_config = {
            "name_template": "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V1.2.0"
        }

        # Mock repository behavior
        self.mock_category_repository.category_exists.return_value = False
        self.mock_category_repository.create_category.return_value = None

        # Act
        result = self.use_case.execute(category_config, test_date)

        # Assert
        self.assertTrue(result['created'])
        self.assertEqual(result['action_taken'], 'created')
        self.assertEqual(result['category_name'],
                        "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ 27 مارس 2025")
        self.assertIsNone(result['error'])

        # Verify repository was called correctly
        self.mock_category_repository.category_exists.assert_called_once()
        self.mock_category_repository.create_category.assert_called_once()

        # Verify the category was created with correct data
        created_category = self.mock_category_repository.create_category.call_args[0][0]
        self.assertIsInstance(created_category, Category)
        self.assertEqual(created_category.template, "{{تصنيف تهذيب شهري}}")

    def test_execute_updates_empty_existing_category(self):
        """Test updating an existing empty category."""
        test_date = datetime(2025, 3, 27)
        category_config = {
            "name_template": "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V1.2.0"
        }

        # Mock repository behavior - category exists but is empty
        self.mock_category_repository.category_exists.return_value = True
        self.mock_category_repository.is_empty_category.return_value = True
        self.mock_category_repository.update_category.return_value = None

        # Act
        result = self.use_case.execute(category_config, test_date)

        # Assert
        self.assertTrue(result['created'])
        self.assertEqual(result['action_taken'], 'updated')
        self.assertIsNone(result['error'])

        # Verify update was called
        self.mock_category_repository.update_category.assert_called_once()

    def test_execute_skips_non_empty_existing_category(self):
        """Test skipping an existing non-empty category."""
        test_date = datetime(2025, 3, 27)
        category_config = {
            "name_template": "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V1.2.0"
        }

        # Mock repository behavior - category exists and is not empty
        self.mock_category_repository.category_exists.return_value = True
        self.mock_category_repository.is_empty_category.return_value = False

        # Act
        result = self.use_case.execute(category_config, test_date)

        # Assert
        self.assertFalse(result['created'])
        self.assertEqual(result['action_taken'], 'skipped')
        self.assertIsNone(result['error'])

        # Verify neither create nor update was called
        self.mock_category_repository.create_category.assert_not_called()
        self.mock_category_repository.update_category.assert_not_called()


if __name__ == '__main__':
    unittest.main()