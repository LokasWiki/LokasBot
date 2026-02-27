"""
Football biography infobox parser implementation.
"""

import logging
from typing import Dict, Any
from .base_parser import InfoboxParser

logger = logging.getLogger(__name__)


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
            import wikitextparser as wtp
            parsed = wtp.parse(wikitext)

            # Find the football biography template
            football_bio_template = self._find_template(parsed)

            if football_bio_template:
                logger.info("Found Infobox football biography template")

                # Extract arguments from the template
                infobox_data = self._extract_template_arguments(
                    football_bio_template)

                count = len(infobox_data)
                msg = "Extracted {} fields from football biography infobox"
                logger.info(msg.format(count))
            else:
                msg = ("No Infobox football biography template found in the "
                       "page")
                logger.warning(msg)

        except Exception as e:
            msg = "Error extracting football biography infobox: {}"
            logger.error(msg.format(e))

        return infobox_data