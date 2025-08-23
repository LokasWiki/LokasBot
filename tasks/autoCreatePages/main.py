"""
Main entry point for the autoCreatePages task.

This module follows the Clean Architecture pattern, orchestrating the
domain layer, data layer, and presentation layer to execute the
monthly page creation and block category creation functionality.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Any

from tasks.autoCreatePages.domain.use_cases.create_monthly_pages import (
    CreateMonthlyPages
)
from tasks.autoCreatePages.domain.use_cases.create_block_category import (
    CreateBlockCategory
)
from tasks.autoCreatePages.data.wiki_page_repository import WikiPageRepository
from tasks.autoCreatePages.data.wiki_category_repository import (
    WikiCategoryRepository
)
from tasks.autoCreatePages.presentation.wiki_operations import WikiOperations


def setup_logging() -> None:
    """Setup logging configuration for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('autoCreatePages.log'),
            logging.StreamHandler()
        ]
    )


def get_page_configurations() -> List[Dict[str, Any]]:
    """
    Get the page configurations for monthly maintenance pages.

    Returns:
        List[Dict[str, Any]]: List of page configurations with templates
        and creation messages
    """
    return [
        {
            "name_template": "تصنيف:صفحات تحتاج إلى مراجعة الترجمة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:صفحات للحذف منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:صفحات نقاش حذف غير مغلقة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بحاجة لتدقيق خبير منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بحاجة للتحديث منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بحاجة للتقسيم منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بحاجة للتنسيق منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بدون مصدر منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات بها وصلات داخلية قليلة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات ذات عبارات بحاجة لمصادر منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات غير مراجعة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات فيها عبارات متقادمة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات للتدقيق اللغوي منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات مترجمة آليا منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات مطلوب توسيعها منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات يتيمة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:تصنيفات تهذيب منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مقالات غير مصنفة منذ MONTH YEAR",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
        {
            "name_template": "تصنيف:مراجعات الزملاء MONTH YEAR",
            "template": "{{تصنيف مخفي}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V2.2.0"
        },
    ]


def get_block_category_config() -> Dict[str, Any]:
    """
    Get the configuration for the block user category.

    Returns:
        Dict[str, Any]: Block category configuration
    """
    return {
        "name_template": "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER",
        "template": "{{تصنيف تهذيب شهري}}",
        "creation_message": "بوت:إنشاء صفحات مطلوبة V1.2.0"
    }


def main():
    """
    Main entry point for the autoCreatePages task.

    This function orchestrates the creation of monthly maintenance pages
    and block user categories using the Clean Architecture pattern.
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize presentation layer
        wiki_ops = WikiOperations(site_name="ar")

        # Validate execution conditions
        date_info = wiki_ops.get_current_date_info()
        logger.info(f"Current date: {date_info['day']}/{date_info['month']}/{date_info['year']}")

        # if not wiki_ops.is_first_day_of_month():
        #     raise Exception("Script can only run on the first day of the month")

        if not date_info['month_name']:
            raise Exception("Invalid month name")

        # Initialize data layer
        site = wiki_ops.get_site()
        page_repository = WikiPageRepository(site)
        category_repository = WikiCategoryRepository(site)

        # Initialize domain layer (use cases)
        create_monthly_pages = CreateMonthlyPages(page_repository)
        create_block_category = CreateBlockCategory(category_repository)

        # Execute monthly pages creation
        logger.info("Starting monthly pages creation...")
        page_configs = get_page_configurations()
        pages_result = create_monthly_pages.execute(
            page_configs,
            date_info['datetime']
        )

        logger.info(f"Monthly pages creation completed: {pages_result}")

        # Execute block category creation
        logger.info("Starting block category creation...")
        block_config = get_block_category_config()
        category_result = create_block_category.execute(
            block_config,
            date_info['datetime']
        )

        logger.info(f"Block category creation completed: {category_result}")

        # Log final results
        logger.info("=== AUTO CREATE PAGES TASK COMPLETED SUCCESSFULLY ===")
        logger.info(f"Pages created: {len(pages_result['created_pages'])}")
        logger.info(f"Pages skipped: {len(pages_result['skipped_pages'])}")
        logger.info(f"Pages errors: {len(pages_result['errors'])}")
        logger.info(f"Block category action: {category_result['action_taken']}")

    except Exception as e:
        logger.error(f"Task failed with error: {e}")
        raise


if __name__ == "__main__":
    main()