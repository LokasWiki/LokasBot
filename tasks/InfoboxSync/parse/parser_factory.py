"""
Factory class for creating infobox parsers using Factory Pattern.
"""

from .base_parser import InfoboxParser
from .football_parser import FootballBiographyParser


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
            from .generic_parser import GenericInfoboxParser
            return GenericInfoboxParser("infobox person")
        elif template_type.lower() == 'biography':
            from .generic_parser import GenericInfoboxParser
            return GenericInfoboxParser("infobox biography")
        else:
            # For custom template names, create generic parser
            from .generic_parser import GenericInfoboxParser
            return GenericInfoboxParser(template_type)

    @staticmethod
    def get_supported_types() -> list:
        """
        Get list of supported template types.

        Returns:
            list: List of supported template type strings
        """
        return [
            'football_biography',
            'person',
            'biography'
        ]