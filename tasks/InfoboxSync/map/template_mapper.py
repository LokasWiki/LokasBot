"""
Template mapper classes for mapping English infobox fields to Arabic equivalents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .field_mappers import FieldMapperFactory, FieldMapper, NumberedFieldMapper

logger = logging.getLogger(__name__)


class TemplateMapper(ABC):
    """
    Abstract base class for template-specific field mapping.
    Each template type (football biography, person, etc.) has its own mapper.
    """

    def __init__(self, template_name: str):
        """
        Initialize the template mapper.

        Args:
            template_name (str): Name of the template being mapped
        """
        self.template_name = template_name
        self.field_mappings = self._get_field_mappings()

    @abstractmethod
    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """
        Get field mappings for this template type.

        Returns:
            Dict[str, Dict[str, Any]]: Mapping configuration with format:
            {
                "english_field_name": {
                    "arabic_key": "الاسم",
                    "field_type": "text|number|image|link|mixed|numbered"
                }
            }
        """
        pass

    def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map all infobox fields using the configured field mappers.

        Args:
            infobox_data (Dict[str, Any]): Raw infobox data from parser

        Returns:
            Dict[str, Any]: Mapped data with Arabic field names
        """
        logger.info("Mapping infobox fields for template: {}".format(
            self.template_name))

        mapped_data = {}
        mapped_fields = {}

        # Handle numbered fields first (they need access to all data)
        numbered_mappings = {}
        for english_key, mapping_config in self.field_mappings.items():
            if mapping_config["field_type"] == "numbered":
                numbered_mappings[english_key] = mapping_config

        for base_key, mapping_config in numbered_mappings.items():
            arabic_key = mapping_config["arabic_key"]
            item_type = mapping_config.get("item_type", "text")

            # Create numbered field mapper
            numbered_mapper = NumberedFieldMapper(base_key, arabic_key, item_type)

            # Map all numbered fields for this base key
            try:
                mapped_field = numbered_mapper.map_numbered_fields(infobox_data)
                mapped_fields.update(mapped_field)

                logger.debug("Mapped numbered field '{}' -> '{}'".format(
                    base_key, arabic_key))

            except Exception as e:
                logger.warning("Failed to map numbered field '{}': {}".format(
                    base_key, e))

        # Handle regular fields
        for english_key, value in infobox_data.items():
            # Skip if this key was already handled as part of numbered fields
            is_numbered_field = False
            for base_key in numbered_mappings.keys():
                if english_key.startswith(base_key):
                    is_numbered_field = True
                    break

            if is_numbered_field:
                continue

            # Normalize the key
            normalized_key = english_key.lower().replace(' ', '_').replace('-', '_')

            # Check if we have a mapping for this field
            if normalized_key in self.field_mappings:
                mapping_config = self.field_mappings[normalized_key]
                arabic_key = mapping_config["arabic_key"]
                field_type = mapping_config["field_type"]

                # Create appropriate field mapper
                field_mapper = FieldMapperFactory.create_mapper(
                    english_key, arabic_key, field_type
                )

                # Map the field
                try:
                    mapped_field = field_mapper.map_field(str(value))
                    mapped_fields.update(mapped_field)

                    logger.debug("Mapped field '{}' -> '{}' (type: {})".format(
                        english_key, arabic_key, field_type))

                except Exception as e:
                    logger.warning("Failed to map field '{}': {}".format(
                        english_key, e))
                    # Fall back to text mapping
                    text_mapper = FieldMapperFactory.create_mapper(
                        english_key, arabic_key, "text"
                    )
                    mapped_field = text_mapper.map_field(str(value))
                    mapped_fields.update(mapped_field)

            else:
                logger.debug("No mapping found for field '{}', skipping".format(
                    english_key))

        mapped_data["mapped_fields"] = mapped_fields
        mapped_data["template_name"] = self.template_name
        mapped_data["total_mapped_fields"] = len(mapped_fields)
        mapped_data["original_field_count"] = len(infobox_data)

        logger.info("Successfully mapped {} fields from {} original fields".format(
            len(mapped_fields), len(infobox_data)))

        return mapped_data

    def get_supported_fields(self) -> List[str]:
        """
        Get list of supported English field names.

        Returns:
            List[str]: List of supported field names
        """
        return list(self.field_mappings.keys())

    def get_field_info(self, english_key: str) -> Dict[str, Any]:
        """
        Get information about a specific field mapping.

        Args:
            english_key (str): English field name

        Returns:
            Dict[str, Any]: Field mapping information or empty dict if not found
        """
        normalized_key = english_key.lower().replace(' ', '_').replace('-', '_')
        return self.field_mappings.get(normalized_key, {})


class FootballBiographyMapper(TemplateMapper):
    """
    Mapper for football biography infobox templates.
    Maps English fields to Arabic equivalents with appropriate field types.
    Handles both regular fields and numbered sequences (years1, clubs1, etc.).
    """

    def __init__(self):
        super().__init__("football_biography")

    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get field mappings for football biography template."""
        return {
            # Personal Information
            "name": {"arabic_key": "اسم", "field_type": "text"},
            "fullname": {"arabic_key": "الاسم الكامل", "field_type": "text"},
            "full_name": {"arabic_key": "الاسم الكامل", "field_type": "text"},
            "image": {"arabic_key": "صورة", "field_type": "image"},
            "upright": {"arabic_key": "حجم الصورة", "field_type": "number"},
            "caption": {"arabic_key": "تعليق الصورة", "field_type": "raw"},
            "birth_date": {"arabic_key": "تاريخ الولادة", "field_type": "raw"},
            "birth_place": {"arabic_key": "مكان الولادة", "field_type": "raw"},
            "death_date": {"arabic_key": "تاريخ الوفاة", "field_type": "raw"},
            "death_place": {"arabic_key": "مكان الوفاة", "field_type": "raw"},
            "height": {"arabic_key": "الطول", "field_type": "number"},
            "position": {"arabic_key": "المركز", "field_type": "raw"},
            # Club Career
            "clubnumber": {"arabic_key": "الرقم بالنادي", "field_type": "number"},
            "youthclubs": {"arabic_key": "أندية_الشباب", "field_type": "numbered", "item_type": "raw"},
            "youthyears": {"arabic_key": "سنوات_الشباب", "field_type": "numbered", "item_type": "raw"},
            "clubs": {"arabic_key": "أندية", "field_type": "numbered", "item_type": "raw"},
            "years": {"arabic_key": "سنوات", "field_type": "numbered", "item_type": "raw"},
            "caps": {"arabic_key": "مباريات", "field_type": "numbered", "item_type": "number"},
            "goals": {"arabic_key": "أهداف", "field_type": "numbered", "item_type": "number"},
            "totalcaps": {"arabic_key": "مجموع_مباريات", "field_type": "number"},
            "totalgoals": {"arabic_key": "إجمالي الأهداف", "field_type": "number"},
            "club-update": {"arabic_key": "تحديث الأندية", "field_type": "raw"},
            "pcupdate": {"arabic_key": "تحديث الأندية", "field_type": "raw"},
            # National Team Career
            "nationalteam": {"arabic_key": "منتخب_وطني", "field_type": "numbered", "item_type": "raw"},
            "nationalyears": {"arabic_key": "سنوات_وطنية", "field_type": "numbered", "item_type": "raw"},
            "nationalcaps": {"arabic_key": "مباريات_وطنية", "field_type": "numbered", "item_type": "number"},
            "nationalgoals": {"arabic_key": "أهداف_وطنية", "field_type": "numbered", "item_type": "number"},
            "nationalteam-update": {"arabic_key": "تحديث المنتخب", "field_type": "raw"},
            "ntupdate": {"arabic_key": "تحديث المنتخب", "field_type": "raw"},
            # Managerial Career
            "managerclubs": {"arabic_key": "أندية_مدرب", "field_type": "numbered", "item_type": "raw"},
            "manageryears": {"arabic_key": "سنوات_مدرب", "field_type": "numbered", "item_type": "raw"},
            # Honors
            "medaltemplates": {"arabic_key": "ميداليات", "field_type": "mixed"},
        }


class GenericTemplateMapper(TemplateMapper):
    """
    Generic mapper for templates without specific field mappings.
    Falls back to text mapping for all fields.
    """

    def __init__(self, template_name: str):
        self.custom_template_name = template_name
        super().__init__(template_name)

    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """
        Generic mapper returns empty dict - all fields will be skipped
        unless custom mappings are provided.
        """
        # This could be extended to load mappings from config files
        return {}


class TemplateMapperFactory:
    """
    Factory for creating appropriate template mappers.
    """

    @staticmethod
    def create_mapper(template_type: str) -> TemplateMapper:
        """
        Create appropriate template mapper based on type.

        Args:
            template_type (str): Type of template ('football_biography', etc.)

        Returns:
            TemplateMapper: Appropriate template mapper instance
        """
        template_type = template_type.lower()

        if template_type == 'football_biography':
            return FootballBiographyMapper()
        elif template_type == 'person':
            return GenericTemplateMapper("person")
        elif template_type == 'biography':
            return GenericTemplateMapper("biography")
        else:
            # For custom template names, create generic mapper
            return GenericTemplateMapper(template_type)

    @staticmethod
    def get_supported_templates() -> List[str]:
        """
        Get list of supported template types.

        Returns:
            List[str]: List of supported template type strings
        """
        return [
            'football_biography',
            'person',
            'biography'
        ]