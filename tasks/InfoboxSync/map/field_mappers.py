"""
Field mapping strategies for different data types in Wikipedia infoboxes.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class FieldMapper(ABC):
    """
    Abstract base class for field mapping strategies.
    Each field type (text, number, image, link, mixed) has its own mapper.
    """

    def __init__(self, english_key: str, arabic_key: str, field_type: str):
        """
        Initialize the field mapper.

        Args:
            english_key (str): English field name from infobox
            arabic_key (str): Corresponding Arabic field name
            field_type (str): Type of field (text, number, image, link, mixed)
        """
        self.english_key = english_key
        self.arabic_key = arabic_key
        self.field_type = field_type

    @abstractmethod
    def map_field(self, value: str) -> Dict[str, Any]:
        """
        Map a field value to the standardized format.

        Args:
            value (str): Raw field value from infobox

        Returns:
            Dict[str, Any]: Mapped field data with Arabic key
        """
        pass

    def _clean_value(self, value: str) -> str:
        """Clean and normalize field value."""
        if not value:
            return ""
        return value.strip()


class NumberedFieldMapper(FieldMapper):
    """
    Mapper for numbered fields that follow a pattern (field1, field2, field3, ...).
    Groups related numbered fields into arrays/lists.
    """

    def __init__(self, base_english_key: str, arabic_key: str, field_type: str = "text"):
        # Store the base key without number (e.g., "years" not "years1")
        self.base_english_key = base_english_key
        super().__init__(base_english_key, arabic_key, "numbered")
        self.item_field_type = field_type

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map numbered field - this is handled by the template mapper."""
        # This method is not used directly for numbered fields
        # The template mapper handles the grouping logic
        return {}

    def map_numbered_fields(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map all numbered fields for this base key.

        Args:
            infobox_data: All infobox fields

        Returns:
            Dict with Arabic key containing array of numbered field values
        """
        numbered_values = []

        # Find all fields that match the pattern: base_key + number
        for key, value in infobox_data.items():
            if key.startswith(self.base_english_key):
                # Extract the number from the key
                number_part = key[len(self.base_english_key):]
                if number_part.isdigit():
                    number = int(number_part)
                    numbered_values.append({
                        "number": number,
                        "value": value,
                        "original_key": key
                    })

        # Sort by number
        numbered_values.sort(key=lambda x: x["number"])

        # Extract just the values in order
        values_only = [item["value"] for item in numbered_values]

        return {
            self.arabic_key: {
                "value": values_only,
                "type": "numbered",
                "item_type": self.item_field_type,
                "count": len(values_only),
                "original_keys": [item["original_key"] for item in numbered_values]
            }
        }


class TextFieldMapper(FieldMapper):
    """
    Mapper for text fields (names, descriptions, etc.).
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "text")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map text field value."""
        clean_value = self._clean_value(value)

        return {
            self.arabic_key: {
                "value": clean_value,
                "type": "text",
                "original_key": self.english_key,
                "validation": self._validate_text(clean_value)
            }
        }

    def _validate_text(self, value: str) -> Dict[str, Any]:
        """Validate text field."""
        return {
            "is_valid": len(value) > 0,
            "length": len(value),
            "has_special_chars": bool(re.search(r'[^\w\s]', value))
        }


class NumberFieldMapper(FieldMapper):
    """
    Mapper for numeric fields (ages, years, counts, etc.).
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "number")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map numeric field value."""
        clean_value = self._clean_value(value)
        numeric_value = self._extract_number(clean_value)

        return {
            self.arabic_key: {
                "value": numeric_value,
                "type": "number",
                "original_key": self.english_key,
                "validation": self._validate_number(clean_value),
                "numeric_value": numeric_value
            }
        }

    def _extract_number(self, value: str) -> Optional[float]:
        """Extract numeric value from string."""
        if not value:
            return None

        # Remove common wiki formatting
        value = re.sub(r'\[\[|\]\]', '', value)
        value = re.sub(r'<[^>]+>', '', value)

        # Find first number (integer or decimal)
        match = re.search(r'(\d+(?:\.\d+)?)', value)
        if match:
            return float(match.group(1))
        return None

    def _validate_number(self, value: str) -> Dict[str, Any]:
        """Validate numeric field."""
        numeric_value = self._extract_number(value)
        return {
            "is_valid": numeric_value is not None,
            "numeric_value": numeric_value,
            "has_units": bool(re.search(r'\d+\s*\w+', value))
        }


class ImageFieldMapper(FieldMapper):
    """
    Mapper for image fields.
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "image")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map image field value."""
        clean_value = self._clean_value(value)
        image_info = self._parse_image(clean_value)

        return {
            self.arabic_key: {
                "value": image_info["filename"],
                "type": "image",
                "original_key": self.english_key,
                "validation": self._validate_image(clean_value),
                "image_info": image_info
            }
        }

    def _parse_image(self, value: str) -> Dict[str, Any]:
        """Parse image field to extract filename and caption."""
        if not value:
            return {"filename": "", "caption": ""}

        # Handle wiki image syntax [[File:filename.jpg|caption]]
        file_match = re.search(r'\[\[File:([^|\]]+)(?:\|([^]]+))?\]\]', value, re.IGNORECASE)
        if file_match:
            return {
                "filename": file_match.group(1),
                "caption": file_match.group(2) or ""
            }

        # Handle simple filename
        return {"filename": value, "caption": ""}

    def _validate_image(self, value: str) -> Dict[str, Any]:
        """Validate image field."""
        image_info = self._parse_image(value)
        return {
            "is_valid": bool(image_info["filename"]),
            "has_caption": bool(image_info["caption"]),
            "filename": image_info["filename"]
        }


class LinkFieldMapper(FieldMapper):
    """
    Mapper for link fields (internal/external links).
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "link")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map link field value."""
        clean_value = self._clean_value(value)
        link_info = self._parse_link(clean_value)

        return {
            self.arabic_key: {
                "value": link_info["url"],
                "type": "link",
                "original_key": self.english_key,
                "validation": self._validate_link(clean_value),
                "link_info": link_info
            }
        }

    def _parse_link(self, value: str) -> Dict[str, Any]:
        """Parse link to extract URL and display text."""
        if not value:
            return {"url": "", "display_text": "", "is_external": False}

        # Handle wiki internal links [[Page|Display Text]]
        internal_match = re.search(r'\[\[([^|\]]+)(?:\|([^]]+))?\]\]', value)
        if internal_match:
            return {
                "url": internal_match.group(1),
                "display_text": internal_match.group(2) or internal_match.group(1),
                "is_external": False
            }

        # Handle external links [http://example.com Display Text]
        external_match = re.search(r'\[([^\s]+)(?:\s([^]]+))?\]', value)
        if external_match:
            return {
                "url": external_match.group(1),
                "display_text": external_match.group(2) or external_match.group(1),
                "is_external": True
            }

        # Plain text that might be a URL
        if value.startswith(('http://', 'https://')):
            return {
                "url": value,
                "display_text": value,
                "is_external": True
            }

        return {"url": value, "display_text": value, "is_external": False}

    def _validate_link(self, value: str) -> Dict[str, Any]:
        """Validate link field."""
        link_info = self._parse_link(value)
        is_valid_url = False

        if link_info["is_external"]:
            try:
                parsed = urlparse(link_info["url"])
                is_valid_url = bool(parsed.netloc)
            except:
                is_valid_url = False

        return {
            "is_valid": bool(link_info["url"]),
            "is_external": link_info["is_external"],
            "is_valid_url": is_valid_url,
            "has_display_text": link_info["display_text"] != link_info["url"]
        }


class MixedFieldMapper(FieldMapper):
    """
    Mapper for mixed content fields (containing multiple data types).
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "mixed")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map mixed field value."""
        clean_value = self._clean_value(value)
        parsed_content = self._parse_mixed_content(clean_value)

        return {
            self.arabic_key: {
                "value": clean_value,
                "type": "mixed",
                "original_key": self.english_key,
                "validation": self._validate_mixed(clean_value),
                "parsed_content": parsed_content
            }
        }

    def _parse_mixed_content(self, value: str) -> Dict[str, Any]:
        """Parse mixed content to identify different elements."""
        if not value:
            return {"text_parts": [], "links": [], "images": [], "numbers": []}

        text_parts = []
        links = []
        images = []
        numbers = []

        # Find links
        link_matches = re.findall(r'\[\[[^\]]+\]\]', value)
        links.extend(link_matches)

        # Find images
        image_matches = re.findall(r'\[\[File:[^\]]+\]\]', value, re.IGNORECASE)
        images.extend(image_matches)

        # Find numbers
        number_matches = re.findall(r'\d+(?:\.\d+)?', value)
        numbers.extend(number_matches)

        # Remove wiki markup for clean text
        clean_text = re.sub(r'\[\[[^\]]+\]\]', '', value)
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        text_parts = [part.strip() for part in clean_text.split() if part.strip()]

        return {
            "text_parts": text_parts,
            "links": links,
            "images": images,
            "numbers": numbers
        }

    def _validate_mixed(self, value: str) -> Dict[str, Any]:
        """Validate mixed field."""
        parsed = self._parse_mixed_content(value)
        return {
            "is_valid": len(value) > 0,
            "has_links": len(parsed["links"]) > 0,
            "has_images": len(parsed["images"]) > 0,
            "has_numbers": len(parsed["numbers"]) > 0,
            "text_parts_count": len(parsed["text_parts"])
        }

class RawFieldMapper(FieldMapper):
    """
    Mapper for raw fields that takes the value as is without any preprocessing.
    """

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "raw")

    def map_field(self, value: str) -> Dict[str, Any]:
        """Map raw field value without any processing."""
        return {
            self.arabic_key: {
                "value": value,
                "type": "raw",
                "original_key": self.english_key,
                "validation": {"is_valid": True}
            }
        }



class FieldMapperFactory:
    """
    Factory for creating appropriate field mappers.
    """

    @staticmethod
    def create_mapper(english_key: str, arabic_key: str, field_type: str) -> FieldMapper:
        """
        Create appropriate field mapper based on type.

        Args:
            english_key (str): English field name
            arabic_key (str): Arabic field name
            field_type (str): Type of field mapper to create

        Returns:
            FieldMapper: Appropriate field mapper instance
        """
        field_type = field_type.lower()
        if field_type == "text":
            return TextFieldMapper(english_key, arabic_key)
        elif field_type == "number":
            return NumberFieldMapper(english_key, arabic_key)
        elif field_type == "image":
            return ImageFieldMapper(english_key, arabic_key)
        elif field_type == "link":
            return LinkFieldMapper(english_key, arabic_key)
        elif field_type == "mixed":
            return MixedFieldMapper(english_key, arabic_key)
        elif field_type == "numbered":
            return NumberedFieldMapper(english_key, arabic_key)
        elif field_type == "raw":
            return RawFieldMapper(english_key, arabic_key)
        else:
            # Default to text mapper
            return TextFieldMapper(english_key, arabic_key)