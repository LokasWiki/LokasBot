"""
Signature scanner implementation for medal distribution.

This module provides a concrete implementation of the SignatureRepository
interface using regex-based text scanning for signature extraction.
"""

import logging
import re
from typing import List
import wikitextparser as wtp
import pywikibot

from tasks.distribute_medals.domain.entities.signature import Signature
from tasks.distribute_medals.domain.repositories.signature_repository import SignatureRepository


class SignatureScanner(SignatureRepository):
    """
    Regex-based implementation of SignatureRepository.

    This class handles signature extraction from wiki pages using
    regex patterns and text parsing.
    """

    def __init__(self, pattern: str = r"\*(?P<signature>.*?)(?=\*|$)"):
        """
        Initialize the signature scanner.

        Args:
            pattern (str): Regex pattern for signature extraction
        """
        self.pattern = pattern
        self.logger = logging.getLogger(__name__)

    def fetch_signatures(self, page_title: str) -> List[Signature]:
        """
        Fetch signatures from a wiki page.

        Args:
            page_title (str): The title of the page containing signatures

        Returns:
            List[Signature]: List of signatures found

        Raises:
            Exception: If the operation fails
        """
        try:
            self.logger.info(f"Fetching signatures from page: {page_title}")

            # Get the wiki site and page
            site = pywikibot.Site()
            page = pywikibot.Page(site, page_title)

            if not page.exists():
                self.logger.warning(f"Page {page_title} does not exist")
                return []

            # Get page text
            text = page.text

            # Find signatures using regex
            matches = re.finditer(self.pattern, text, re.MULTILINE)

            signatures = []
            for match in matches:
                signature_text = match.groupdict().get('signature', '').strip()
                if signature_text:
                    try:
                        # Extract username from signature
                        username = self._extract_username(signature_text)
                        signature = Signature(signature_text, username)
                        signatures.append(signature)
                    except Exception as e:
                        self.logger.warning(f"Failed to create signature: {str(e)}")

            self.logger.info(f"Found {len(signatures)} signatures")
            return signatures

        except Exception as e:
            error_msg = f"Failed to fetch signatures from {page_title}: {str(e)}"
            self.logger.error(error_msg)
            raise

    def get_random_signature(self, exclude_username: str = None) -> Signature:
        """
        Get a random signature, optionally excluding a specific username.

        Args:
            exclude_username (str, optional): Username to exclude from selection

        Returns:
            Signature: A random signature

        Raises:
            Exception: If no signatures are available
        """
        try:
            # Get signatures from the default page
            signatures = self.fetch_signatures("ويكيبيديا:توزيع أوسمة/تواقيع")

            if not signatures:
                self.logger.warning("No signatures found")
                return Signature.create_default()

            # Filter out excluded username
            if exclude_username:
                filtered_signatures = [
                    sig for sig in signatures
                    if sig.user_name != exclude_username
                ]
                if filtered_signatures:
                    signatures = filtered_signatures

            # Return a random signature
            import random
            signature = random.choice(signatures)
            self.logger.info(f"Selected signature from user: {signature.user_name}")
            return signature

        except Exception as e:
            self.logger.error(f"Failed to get random signature: {str(e)}")
            return Signature.create_default()

    def validate_signature(self, signature: Signature) -> bool:
        """
        Validate a signature.

        Args:
            signature (Signature): The signature to validate

        Returns:
            bool: True if the signature is valid
        """
        return signature.is_valid

    def get_signature_count(self) -> int:
        """
        Get the total count of available signatures.

        Returns:
            int: Number of available signatures
        """
        try:
            signatures = self.fetch_signatures("ويكيبيديا:توزيع أوسمة/تواقيع")
            return len(signatures)
        except Exception as e:
            self.logger.error(f"Failed to get signature count: {str(e)}")
            return 0

    def _extract_username(self, signature_text: str) -> str:
        """
        Extract username from signature text.

        Args:
            signature_text (str): The signature text

        Returns:
            str: The extracted username
        """
        try:
            # Parse the signature text
            parsed = wtp.parse(signature_text)

            # Find the first wikilink (usually the user link)
            for link in parsed.wikilinks:
                if link.title.startswith("مستخدم:"):
                    # Extract username from namespace:title format
                    namespace, username = link.title.split(":", 1)
                    return username

            # Fallback: try to extract from common patterns
            patterns = [
                r"مستخدم:([^|\]]+)",
                r"User:([^|\]]+)",
                r"\[\[([^|\]]+)\]\]"
            ]

            for pattern in patterns:
                match = re.search(pattern, signature_text)
                if match:
                    username = match.group(1)
                    if "مستخدم:" in username:
                        username = username.split(":", 1)[1]
                    return username

            # If no username found, return a default
            return "Unknown"

        except Exception as e:
            self.logger.warning(f"Failed to extract username: {str(e)}")
            return "Unknown"