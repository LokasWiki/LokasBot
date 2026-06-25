"""
Arabic Wikipedia template builder implementation.
"""

import logging
from typing import Dict, Any, List, Optional
from .base_builder import TemplateBuilder, TemplateBuilderFactory, BuildResult

logger = logging.getLogger(__name__)


class ArabicTemplateBuilder(TemplateBuilder):
    """Builder for Arabic Wikipedia templates using translated data."""

    def __init__(self, template_type: str = 'football_biography'):
        """
        Initialize Arabic template builder.

        Args:
            template_type (str): Type of template to build
        """
        super().__init__(template_type)
        self.field_formatters = {
            'text': self._format_text_field,
            'number': self._format_number_field,
            'link': self._format_link_field,
            'image': self._format_image_field,
            'numbered': self._format_numbered_field,
            'mixed': self._format_mixed_field
        }

    def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult:
        """
        Build an Arabic Wikipedia template from translated data.

        Args:
            translated_data (Dict[str, Any]): Data from translate stage with translated_fields
            **kwargs: Additional parameters

        Returns:
            BuildResult: Template building result
        """
        try:
            logger.info(f"Building Arabic template for type: {self.template_type}")

            # Extract translated fields
            translated_fields = translated_data.get('translated_fields', {})
            if not translated_fields:
                return BuildResult(
                    template_text="",
                    template_type=self.template_type,
                    field_count=0,
                    success=False,
                    metadata={},
                    errors=["No translated fields found"]
                )

            # Build template structure
            template_lines = []
            template_lines.append(f"{{{{{self.get_template_name()}")
            template_lines.append("|")  # First pipe after template name

            # Process each translated field
            field_count = 0
            errors = []

            for arabic_key, field_data in translated_fields.items():
                try:
                    # Get the translated value
                    if 'translated_value' in field_data:
                        value = field_data['translated_value']
                    else:
                        value = field_data.get('value', '')

                    # Format the field
                    formatted_field = self.format_field(arabic_key, {
                        'value': value,
                        'type': field_data.get('type', 'text'),
                        'original_type': field_data.get('type', 'text')
                    })

                    if formatted_field:
                        # Handle different field types
                        if field_data.get('type') == 'numbered' and isinstance(formatted_field, list):
                            # Numbered fields return a list of lines
                            template_lines.extend(formatted_field)
                            field_count += 1
                        elif isinstance(formatted_field, str) and formatted_field.strip():
                            template_lines.append(formatted_field)
                            field_count += 1

                except Exception as e:
                    error_msg = f"Failed to format field {arabic_key}: {e}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                    continue

            # Close template
            template_lines.append("}}")

            # Join all lines with actual newlines - creates proper line breaks
            template_text = "\n".join(template_lines)

            logger.info(f"Successfully built Arabic template with {field_count} fields")

            return BuildResult(
                template_text=template_text,
                template_type=self.template_type,
                field_count=field_count,
                success=True,
                metadata={
                    'template_name': self.get_template_name(),
                    'builder_name': self.get_builder_name(),
                    'total_input_fields': len(translated_fields)
                },
                errors=errors
            )

        except Exception as e:
            logger.error(f"Template building failed: {e}")
            return BuildResult(
                template_text="",
                template_type=self.template_type,
                field_count=0,
                success=False,
                metadata={},
                errors=[str(e)]
            )

    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """
        Format a single field for the Arabic template.

        Args:
            arabic_key (str): Arabic field name
            field_data (Dict[str, Any]): Field data with value and type

        Returns:
            str: Formatted field string
        """
        field_type = field_data.get('type', 'text')

        # Get the appropriate formatter
        formatter = self.field_formatters.get(field_type, self._format_text_field)

        try:
            return formatter(arabic_key, field_data)
        except Exception as e:
            logger.warning(f"Failed to format field {arabic_key} of type {field_type}: {e}")
            # Fallback to text formatting
            return self._format_text_field(arabic_key, field_data)

    def _format_text_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """Format a text field."""
        value = field_data.get('value', '')
        if not value:
            return ""

        # Escape pipes and other wiki syntax
        # escaped_value = str(value).replace('|', '{{!}}').replace('=', '{{=}}')
        escaped_value = str(value)

        return f"| {arabic_key} = {escaped_value}"

    def _format_number_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """Format a number field."""
        value = field_data.get('value', '')
        if not value:
            return ""

        # Keep numbers as-is, just ensure proper formatting
        return f"| {arabic_key} = {value}"

    def _format_link_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """Format a link field."""
        value = field_data.get('value', '')
        if not value:
            return ""

        # Ensure proper wiki link format
        if '|' in str(value):
            # Already has link text
            return f"| {arabic_key} = {value}"
        else:
            # Simple link
            return f"| {arabic_key} = [[{value}]]"

    def _format_image_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """Format an image field."""
        value = field_data.get('value', '')
        if not value:
            return ""

        # Ensure proper image format
        if value.startswith('[[File:') or value.startswith('[[ملف:'):
            return f"| {arabic_key} = {value}"
        else:
            return f"| {arabic_key} = [[ملف:{value}]]"

    def _format_numbered_field(self, arabic_key: str, field_data: Dict[str, Any]) -> List[str]:
        """Format a numbered field (array of values)."""
        value = field_data.get('value', [])
        if not value or not isinstance(value, list):
            return []

        # Return a list of formatted lines for each numbered field
        formatted_lines = []

        for i, item_value in enumerate(value, 1):
            if item_value:  # Only include non-empty values
                field_name = f"{arabic_key}{i}"
                # escaped_value = str(item_value).replace('|', '{{!}}').replace('=', '{{=}}')
                escaped_value = str(item_value)
                formatted_lines.append(f"| {field_name} = {escaped_value}")

        return formatted_lines

    def _format_mixed_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """Format a mixed field (contains both text and links)."""
        value = field_data.get('value', '')
        if not value:
            return ""

        # Mixed fields usually contain wiki markup, keep as-is
        return f"| {arabic_key} = {value}"

    def get_template_name(self) -> str:
        """Get the Arabic Wikipedia template name."""
        template_names = {
            'football_biography': 'صندوق معلومات سيرة كرة قدم',
            'person': 'صندوق شخص',
            'biography': 'سيرة شخصية',
            'football_club': 'صندوق نادي كرة قدم',
            'country': 'صندوق دولة',
            'city': 'صندوق مدينة',
            'university': 'صندوق جامعة',
            'company': 'صندوق شركة',
            'film': 'صندوق فيلم',
            'book': 'صندوق كتاب',
            'album': 'صندوق ألبوم',
            'tv_series': 'صندوق مسلسل تلفزيوني'
        }

        return template_names.get(self.template_type, 'صندوق عام')

    def is_available(self) -> bool:
        """Check if Arabic template builder is available."""
        # Always available since it doesn't require external services
        return True

    def get_builder_name(self) -> str:
        """Get the name of this builder."""
        return f"Arabic {self.template_type.title()} Builder"


# Register the Arabic builder
TemplateBuilderFactory.register_builder("arabic", ArabicTemplateBuilder)
TemplateBuilderFactory.register_builder("arabic_football", ArabicTemplateBuilder)