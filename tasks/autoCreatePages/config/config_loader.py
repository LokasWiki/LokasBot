"""
Configuration loader for the autoCreatePages task.

This module provides configuration management functionality to externalize
settings and templates, following the Clean Architecture principle of
keeping configuration separate from business logic.
"""

import json
import os
from typing import Dict, List, Any, Optional


class ConfigLoader:
    """
    Configuration loader for managing externalized settings and templates.

    This class handles loading configuration from various sources including
    JSON files, environment variables, and provides default configurations
    when external files are not available.
    """

    def __init__(self, config_dir: str = None):
        """
        Initialize the ConfigLoader.

        Args:
            config_dir (str, optional): Directory containing configuration files.
                                     If None, uses default location.
        """
        if config_dir is None:
            # Default to the config directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = current_dir

        self.config_dir = config_dir
        self._config_cache = {}

    def get_page_configurations(self) -> List[Dict[str, Any]]:
        """
        Get page configurations from external file or return defaults.

        Returns:
            List[Dict[str, Any]]: List of page configurations
        """
        config_file = os.path.join(self.config_dir, 'pages_config.json')

        if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)
                    self._validate_page_configs(configs)
                    return configs
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Failed to load page config from {config_file}: {e}")
                print("Using default configurations...")

        return self._get_default_page_configurations()

    def get_block_category_config(self) -> Dict[str, Any]:
        """
        Get block category configuration from external file or return defaults.

        Returns:
            Dict[str, Any]: Block category configuration
        """
        config_file = os.path.join(self.config_dir, 'categories_config.json')

        if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._validate_category_config(config)
                    return config
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Failed to load category config from {config_file}: {e}")
                print("Using default configuration...")

        return self._get_default_block_category_config()

    def get_wiki_settings(self) -> Dict[str, Any]:
        """
        Get wiki-specific settings.

        Returns:
            Dict[str, Any]: Wiki settings including site name and timeouts
        """
        return {
            'site_name': 'ar',
            'max_retries': 3,
            'timeout': 30,
            'user_agent': 'autoCreatePages Bot v2.2.0'
        }

    def _validate_page_configs(self, configs: List[Dict[str, Any]]) -> None:
        """
        Validate page configuration structure.

        Args:
            configs (List[Dict[str, Any]]): Configurations to validate

        Raises:
            ValueError: If configuration structure is invalid
        """
        required_keys = {'name_template', 'template', 'creation_message'}

        for i, config in enumerate(configs):
            if not isinstance(config, dict):
                raise ValueError(f"Configuration {i} must be a dictionary")

            missing_keys = required_keys - set(config.keys())
            if missing_keys:
                raise ValueError(f"Configuration {i} missing keys: {missing_keys}")

            # Validate template placeholders
            name_template = config['name_template']
            if 'MONTH' not in name_template or 'YEAR' not in name_template:
                raise ValueError(f"Configuration {i} name_template must contain 'MONTH' and 'YEAR' placeholders")

    def _validate_category_config(self, config: Dict[str, Any]) -> None:
        """
        Validate category configuration structure.

        Args:
            config (Dict[str, Any]): Configuration to validate

        Raises:
            ValueError: If configuration structure is invalid
        """
        required_keys = {'name_template', 'template', 'creation_message'}

        if not isinstance(config, dict):
            raise ValueError("Category configuration must be a dictionary")

        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"Category configuration missing keys: {missing_keys}")

    def _get_default_page_configurations(self) -> List[Dict[str, Any]]:
        """
        Get default page configurations.

        Returns:
            List[Dict[str, Any]]: Default page configurations
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

    def _get_default_block_category_config(self) -> Dict[str, Any]:
        """
        Get default block category configuration.

        Returns:
            Dict[str, Any]: Default block category configuration
        """
        return {
            "name_template": "تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ DATE_PLACEHOLDER",
            "template": "{{تصنيف تهذيب شهري}}",
            "creation_message": "بوت:إنشاء صفحات مطلوبة V1.2.0"
        }