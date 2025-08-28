"""
Parse stage for Wikipedia infobox synchronization using Strategy Pattern.
"""

import logging
from .parser_factory import InfoboxParserFactory

logger = logging.getLogger(__name__)


def parse_data(data: dict, template_type: str = 'football_biography') -> dict:
    """
    Parse the fetched Wikipedia data to extract infobox information.

    Args:
        data (dict): The raw Wikipedia data with page content.
        template_type (str): Type of template to parse ('football_biography',
                          'person', etc.)

    Returns:
        dict: Parsed infobox data.
    """
    logger.info("Starting Wikipedia data parsing for template: {}".format(
        template_type))

    try:
        page_content = data.get('content', '')
        page_title = data.get('title', '')
        arabic_title = data.get('arabic_title', '')

        # Create parser using Strategy Pattern
        parser = InfoboxParserFactory.create_parser(template_type)

        # Parse infobox from Wikipedia content
        infobox_data = parser.parse_infobox(page_content)

        # Extract categories
        categories = extract_categories_from_wikitext(page_content)

        # Extract links (simplified - could be enhanced)
        links = extract_links_from_wikitext(page_content)

        parsed_data = {
            'title': page_title,
            'arabic_title': arabic_title,
            'infobox': infobox_data,
            'categories': categories,
            'links': links,
            'raw_content': page_content
        }

        logger.info("Successfully parsed data for title: {}".format(page_title))
        return parsed_data

    except Exception as e:
        logger.error("Error parsing Wikipedia data: {}".format(e))
        raise


def extract_categories_from_wikitext(wikitext: str) -> list:
    """
    Extract categories from Wikipedia wikitext.

    Args:
        wikitext (str): The raw Wikipedia page content.

    Returns:
        list: List of category names.
    """
    import re
    categories = []

    try:
        # Pattern to match category links
        category_pattern = r'\[\[Category:([^\]]+)\]\]'
        matches = re.findall(category_pattern, wikitext, re.IGNORECASE)

        categories = [match.strip() for match in matches]

    except Exception as e:
        logger.warning("Error extracting categories: {}".format(e))

    return categories


def extract_links_from_wikitext(wikitext: str) -> list:
    """
    Extract internal links from Wikipedia wikitext.

    Args:
        wikitext (str): The raw Wikipedia page content.

    Returns:
        list: List of linked page titles.
    """
    import re
    links = []

    try:
        # Pattern to match internal links [[Link|Display]]
        link_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(link_pattern, wikitext)

        # Filter out special links (File:, Category:, etc.)
        special_prefixes = ('File:', 'Category:', 'Image:', 'Template:')
        links = [match.strip() for match in matches
                 if not match.startswith(special_prefixes)]

    except Exception as e:
        logger.warning("Error extracting links: {}".format(e))

    return links