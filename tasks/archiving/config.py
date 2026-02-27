from typing import Dict, Union, List

# Define constants for configuration keys
TEMPLATE_NAME_KEY = 'template_name_with_namespace'
ARCHIVING_TEMPLATE_KEY = 'automated_archiving_template'
SECTION_TYPE_KEYS = 'section_type'
SKIP_TEMPLATES_KEY = 'skip_templates'

# Define the type for configuration values
ConfigValue = Union[str, int, bool, List[str]]  # Extend as needed

# Define the configuration dictionary
USER_CONFIG: Dict[str, ConfigValue] = {
    TEMPLATE_NAME_KEY: 'قالب:أرشيف_آلي',
    ARCHIVING_TEMPLATE_KEY: 'أرشفة آلية',
    SECTION_TYPE_KEYS: ['حجم', 'قسم'],  # Example list of section types
    SKIP_TEMPLATES_KEY: ['رشف', 'آخر']  # List of skip templates
}
