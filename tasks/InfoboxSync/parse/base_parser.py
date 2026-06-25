"""
Abstract base class for infobox parsers using Strategy Pattern.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
import wikitextparser as wtp

logger = logging.getLogger(__name__)


class InfoboxParser(ABC):
    """
    Abstract base class for infobox parsers using Strategy Pattern.

    This class defines the interface for parsing different types of
    Wikipedia infobox templates using wikitextparser.
    """

    def __init__(self, template_name: str):
        """
        Initialize the parser with the target template name.

        Args:
            template_name (str): Name of the infobox template to parse
        """
        self.template_name = template_name.lower()

    @abstractmethod
    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """
        Parse the infobox from wikitext.

        Args:
            wikitext (str): The raw Wikipedia page content

        Returns:
            Dict[str, Any]: Extracted infobox fields
        """
        pass

    def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template:
        """
        Find the target template in the parsed wikitext.

        Args:
            parsed_wikitext: Parsed wikitext object

        Returns:
            wtp.Template: The found template object, or None
        """
        templates = parsed_wikitext.templates

        for template in templates:
            template_name = template.name.strip().lower()
            if template_name == self.template_name:
                return template

        return None

    def _extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]:
        """
        Extract arguments from a template object.

        Args:
            template: The template object to extract from

        Returns:
            Dict[str, str]: Dictionary of template arguments
        """
        infobox_data = {}

        for argument in template.arguments:
            key = argument.name.strip()
            value = argument.value.strip()

            # Clean up the value by removing markup if needed
            # clean_value = wtp.parse(value).plain_text()
            clean_value = value
            if key and clean_value:
                infobox_data[key] = clean_value

        return infobox_data