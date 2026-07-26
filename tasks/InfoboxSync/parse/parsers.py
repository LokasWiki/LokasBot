"""
Infobox parsers using Strategy Pattern for different template types.
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
            clean_value = wtp.parse(value).plain_text()

            if key and clean_value:
                infobox_data[key] = clean_value

        return infobox_data


class FootballBiographyParser(InfoboxParser):
    """
    Parser for Infobox football biography template.
    """

    def __init__(self):
        super().__init__("infobox football biography")

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """
        Parse football biography infobox from wikitext.

        Args:
            wikitext (str): The raw Wikipedia page content

        Returns:
            Dict[str, Any]: Extracted football biography fields
        """
        infobox_data = {}

        try:
            # Parse wikitext using wikitextparser
            parsed = wtp.parse(wikitext)

            # Find the football biography template
            football_bio_template = self._find_template(parsed)

            if football_bio_template:
                logger.info("Found Infobox football biography template")

                # Extract arguments from the template
                infobox_data = self._extract_template_arguments(football_bio_template)

                logger.info("Extracted {} fields from football biography infobox".format(
                    len(infobox_data)))
            else:
                logger.warning("No Infobox football biography template "
                             "found in the page")

        except Exception as e:
            logger.error("Error extracting football biography infobox: {}".format(e))

        return infobox_data


class GenericInfoboxParser(InfoboxParser):
    """
    Generic parser for any infobox template type.
    """

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """
        Parse generic infobox from wikitext.

        Args:
            wikitext (str): The raw Wikipedia page content

        Returns:
            Dict[str, Any]: Extracted infobox fields
        """
        infobox_data = {}

        try:
            # Parse wikitext using wikitextparser
            parsed = wtp.parse(wikitext)

            # Find the target template
            template = self._find_template(parsed)

            if template:
                logger.info("Found {} template".format(self.template_name))

                # Extract arguments from the template
                infobox_data = self._extract_template_arguments(template)

                logger.info("Extracted {} fields from {} template".format(
                    len(infobox_data), self.template_name))
            else:
                logger.warning("No {} template found in the page".format(
                    self.template_name))

        except Exception as e:
            logger.error("Error extracting {} infobox: {}".format(
                self.template_name, e))

        return infobox_data


class InfoboxParserFactory:
    """
    Factory class to create appropriate parsers based on template type.
    """

    @staticmethod
    def create_parser(template_type: str) -> InfoboxParser:
        """
        Create the appropriate parser for the given template type.

        Args:
            template_type (str): Type of template ('football_biography',
                          'person', etc.)

        Returns:
            InfoboxParser: The appropriate parser instance

        Raises:
            ValueError: If template type is not supported
        """
        if template_type.lower() == 'football_biography':
            return FootballBiographyParser()
        elif template_type.lower() == 'person':
            return GenericInfoboxParser("infobox person")
        elif template_type.lower() == 'biography':
            return GenericInfoboxParser("infobox biography")
        else:
            # For custom template names, create generic parser
            return GenericInfoboxParser(template_type)