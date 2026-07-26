"""
Map stage for Wikipedia infobox synchronization using Strategy Pattern.
"""

import logging
from .template_mapper import TemplateMapperFactory

logger = logging.getLogger(__name__)


def map_data(parsed_data: dict,
             template_type: str = 'football_biography') -> dict:
    """
    Map the parsed data to a standardized format with Arabic field names.

    Args:
        parsed_data (dict): The parsed data from the parse stage.
        template_type (str): Type of template ('football_biography',
                          'person', etc.)

    Returns:
        dict: Mapped data in standardized format with Arabic field names.
    """
    msg = "Starting data mapping for template type: {}".format(template_type)
    logger.info(msg)

    try:
        page_title = parsed_data.get('title', '')
        infobox_data = parsed_data.get('infobox', {})

        # Create appropriate template mapper
        template_mapper = TemplateMapperFactory.create_mapper(template_type)

        # Map the infobox data using the template mapper
        mapped_infobox = template_mapper.map_infobox(infobox_data)

        # Build the final mapped data structure
        mapped_data = {
            'page_title': page_title,
            'template_type': template_type,
            'arabic_fields': mapped_infobox['mapped_fields'],
            'metadata': {
                'categories': parsed_data.get('categories', []),
                'links': parsed_data.get('links', []),
                'template_name': mapped_infobox['template_name'],
                'total_mapped_fields': mapped_infobox['total_mapped_fields'],
                'original_field_count': mapped_infobox['original_field_count']
            },
            'raw_content': parsed_data.get('raw_content', ''),
            'arabic_title': parsed_data.get('arabic_title', '')
        }

        logger.info("Successfully mapped data for: {}".format(page_title))
        msg = ("Mapped {} fields out of {} original fields").format(
            mapped_infobox['total_mapped_fields'],
            mapped_infobox['original_field_count'])
        logger.info(msg)

        return mapped_data

    except Exception as e:
        logger.error("Error mapping data: {}".format(e))
        raise


def get_supported_template_types() -> list:
    """
    Get list of supported template types for mapping.

    Returns:
        list: List of supported template type strings
    """
    return TemplateMapperFactory.get_supported_templates()


def create_field_demo(template_type: str = 'football_biography') -> dict:
    """
    Create a demo showing different field types for a template.

    Args:
        template_type (str): Type of template to create demo for

    Returns:
        dict: Demo data showing different field types
    """
    if template_type == 'football_biography':
        return {
            "name": "Lionel Messi",  # text field
            "height": "1.70 m",      # number field
            # image field
            "image": "[[File:Messi_vs_Nigeria_2018.jpg|Messi playing]]",
            # link field
            "website": "[http://www.messi.com Official Website]",
            # mixed field
            "position": "[[Forward (association football)|Forward]]",
            "clubnumber": "10",     # number field
            "caps1": "520",         # number field
            "goals1": "474"         # number field
        }

    return {}


def demonstrate_field_types():
    """
    Demonstrate how different field types are mapped.
    """
    logger.info("Demonstrating field type mapping...")

    # Create demo data
    demo_data = create_field_demo('football_biography')

    # Map the demo data
    try:
        mapped_result = map_data({
            'title': 'Demo Football Player',
            'infobox': demo_data,
            'categories': ['Football players'],
            'links': ['Argentina national football team'],
            'arabic_title': 'لاعب كرة قدم تجريبي'
        }, 'football_biography')

        logger.info("Demo mapping completed successfully")
        arabic_fields = list(mapped_result['arabic_fields'].keys())
        logger.info("Arabic fields: {}".format(arabic_fields))

        return mapped_result

    except Exception as e:
        logger.error("Demo mapping failed: {}".format(e))
        return {}