"""
Use case for managing signatures for medal distribution.

This use case encapsulates the business logic for signature
management and selection for medal templates.
"""

import logging
from typing import List
from tasks.distribute_medals.domain.entities.signature import Signature
from tasks.distribute_medals.domain.repositories.signature_repository import SignatureRepository


class ManageSignatures:
    """
    Use case for managing signatures.

    This class contains the business logic for signature operations
    including fetching, validation, and selection.
    """

    def __init__(self, signature_repo: SignatureRepository):
        """
        Initialize the ManageSignatures use case.

        Args:
            signature_repo (SignatureRepository): Repository for signature operations
        """
        self.signature_repo = signature_repo
        self.logger = logging.getLogger(__name__)

    def execute_get_random(self, exclude_username: str = None) -> Signature:
        """
        Get a random signature for medal distribution.

        Args:
            exclude_username (str, optional): Username to exclude from selection

        Returns:
            Signature: A random signature

        Raises:
            Exception: If no valid signatures are available
        """
        try:
            self.logger.info("Getting random signature for medal distribution")
            signature = self.signature_repo.get_random_signature(exclude_username)

            if not signature.is_valid:
                raise ValueError("Retrieved signature is not valid")

            self.logger.info(f"Selected signature from user: {signature.user_name}")
            return signature

        except Exception as e:
            self.logger.error(f"Failed to get random signature: {str(e)}")
            # Return default signature as fallback
            return Signature.create_default()

    def execute_fetch_all(self, page_title: str) -> List[Signature]:
        """
        Fetch all signatures from a page.

        Args:
            page_title (str): The title of the page containing signatures

        Returns:
            List[Signature]: List of all signatures found
        """
        try:
            self.logger.info(f"Fetching signatures from page: {page_title}")
            signatures = self.signature_repo.fetch_signatures(page_title)

            valid_signatures = [sig for sig in signatures if sig.is_valid]

            self.logger.info(
                f"Fetched {len(signatures)} signatures, "
                f"{len(valid_signatures)} valid"
            )

            return valid_signatures

        except Exception as e:
            self.logger.error(f"Failed to fetch signatures: {str(e)}")
            return []

    def execute_validate(self, signature: Signature) -> bool:
        """
        Validate a signature.

        Args:
            signature (Signature): The signature to validate

        Returns:
            bool: True if the signature is valid
        """
        try:
            is_valid = self.signature_repo.validate_signature(signature)
            self.logger.info(f"Signature validation: {is_valid}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Signature validation failed: {str(e)}")
            return False

    def execute_get_count(self) -> int:
        """
        Get the total count of available signatures.

        Returns:
            int: Number of available signatures
        """
        try:
            count = self.signature_repo.get_signature_count()
            self.logger.info(f"Available signatures: {count}")
            return count
        except Exception as e:
            self.logger.error(f"Failed to get signature count: {str(e)}")
            return 0