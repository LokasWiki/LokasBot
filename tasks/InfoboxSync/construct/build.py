"""
Build stage for Arabic Wikipedia template construction.
"""

import logging
from typing import Dict, Any, Optional
from .base_builder import TemplateBuilderFactory, BuildResult

logger = logging.getLogger(__name__)


def construct_template(translated_data: dict, builder_name: str = 'arabic',
                      template_type: str = 'football_biography') -> BuildResult:
    """
    Build an Arabic Wikipedia template from translated data.

    Args:
        translated_data (dict): Data from translate stage with translated_fields
        builder_name (str): Name of the builder to use ('arabic', 'arabic_football', etc.)
        template_type (str): Type of template to build

    Returns:
        BuildResult: Template building result with Arabic template text
    """
    logger.info(f"Starting template build with builder: {builder_name}")

    try:
        # Create the appropriate builder
        builder = TemplateBuilderFactory.create_builder(
            builder_name,
            template_type=template_type
        )

        # Check if builder is available
        if not builder.is_available():
            error_msg = f"Template builder {builder_name} is not available"
            logger.error(error_msg)
            return BuildResult(
                template_text="",
                template_type=template_type,
                field_count=0,
                success=False,
                metadata={},
                errors=[error_msg]
            )

        # Build the template
        result = builder.construct_template(translated_data)

        if result.success:
            logger.info(f"Template build completed successfully: {result.field_count} fields")
        else:
            logger.error(f"Template build failed: {result.errors}")

        return result

    except Exception as e:
        logger.error(f"Template building failed: {e}")
        return BuildResult(
            template_text="",
            template_type=template_type,
            field_count=0,
            success=False,
            metadata={},
            errors=[str(e)]
        )


def construct_arabic_template(translated_data: dict, template_type: str = 'football_biography') -> BuildResult:
    """
    Convenience function to build Arabic templates.

    Args:
        translated_data (dict): Translated data from translate stage
        template_type (str): Template type to build

    Returns:
        BuildResult: Arabic template building result
    """
    return construct_template(translated_data, 'arabic', template_type)


def get_available_builders() -> list:
    """
    Get list of available template builders.

    Returns:
        list: List of available builder names
    """
    try:
        return TemplateBuilderFactory.get_available_builders()
    except Exception as e:
        logger.error(f"Error getting available builders: {e}")
        return []


def get_supported_template_types() -> list:
    """
    Get list of supported template types.

    Returns:
        list: List of supported template type names
    """
    try:
        return TemplateBuilderFactory.get_supported_template_types()
    except Exception as e:
        logger.error(f"Error getting supported template types: {e}")
        return []


def test_builder(builder_name: str = 'arabic') -> bool:
    """
    Test if a template builder is available and working.

    Args:
        builder_name (str): Name of the builder to test

    Returns:
        bool: True if builder is available and working
    """
    try:
        builder = TemplateBuilderFactory.create_builder(builder_name)
        return builder.is_available()
    except Exception as e:
        logger.error(f"Error testing builder {builder_name}: {e}")
        return False


def create_sample_arabic_template() -> str:
    """
    Create a sample Arabic Wikipedia template for testing.

    Returns:
        str: Sample Arabic template
    """
    return """{{صندوق سيرة لاعب كرة قدم
| الاسم = بول أباسولو
| الاسم الكامل = بول أباسولو أمانتيغي
| تاريخ الميلاد = 29 يونيو 1984
| مكان الميلاد = دورانغو، إسبانيا
| الطول = 1.84 م
| المركز = مهاجم
| الأندية1 = نادي باسكونيا
| سنوات اللاعب1 = 2002–2003
| المباريات1 = 35
| الأهداف1 = 5
| الأندية2 = براكالدو
| سنوات اللاعب2 = 2003–2004
| المباريات2 = 24
| الأهداف2 = 1
}}"""


def validate_arabic_template(template_text: str) -> Dict[str, Any]:
    """
    Validate an Arabic Wikipedia template.

    Args:
        template_text (str): Template text to validate

    Returns:
        dict: Validation results
    """
    errors = []
    warnings = []

    # Check basic structure
    if not template_text.startswith('{{'):
        errors.append("Template must start with '{{'")
    if not template_text.endswith('}}'):
        errors.append("Template must end with '}}'")

    # Check for required fields (basic validation)
    lines = template_text.split('\n')
    field_count = 0

    for line in lines:
        line = line.strip()
        if line.startswith('|') and '=' in line:
            field_count += 1

    if field_count == 0:
        warnings.append("No fields found in template")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'field_count': field_count,
        'template_length': len(template_text)
    }


def format_template_for_display(template_text: str) -> str:
    """
    Format template text for better display in logs or UI.

    Args:
        template_text (str): Raw template text

    Returns:
        str: Formatted template text
    """
    # Add line numbers and indentation for readability
    lines = template_text.split('\n')
    formatted_lines = []

    for i, line in enumerate(lines, 1):
        if line.strip():
            formatted_lines.append("2d")
        else:
            formatted_lines.append("")

    return '\n'.join(formatted_lines)


def estimate_template_quality(template_text: str) -> Dict[str, Any]:
    """
    Estimate the quality of a generated template.

    Args:
        template_text (str): Template text to analyze

    Returns:
        dict: Quality metrics
    """
    # Basic quality metrics
    field_count = template_text.count('|')
    escaped_chars = template_text.count('{{!}}') + template_text.count('{{=}}')

    # Check for common issues
    issues = []
    if '{{!}}' in template_text:
        issues.append("Contains escaped pipes")
    if '{{=}}' in template_text:
        issues.append("Contains escaped equals signs")
    if '\n\n\n' in template_text:
        issues.append("Multiple consecutive empty lines")

    # Calculate quality score (0-100)
    base_score = min(100, field_count * 10)  # 10 points per field, max 100
    penalty = len(issues) * 10  # 10 point penalty per issue
    quality_score = max(0, base_score - penalty)

    return {
        'quality_score': quality_score,
        'field_count': field_count,
        'escaped_characters': escaped_chars,
        'issues': issues,
        'template_length': len(template_text)
    }