"""
Repository interface for signature operations.

This interface defines the contract for signature-related operations,
following the Repository pattern to abstract signature management.
"""

from abc import ABC, abstractmethod
from typing import List
from tasks.distribute_medals.domain.entities.signature import Signature


class SignatureRepository(ABC):
    """
    Abstract repository interface for signature operations.

    This interface defines the contract for signature-related operations,
    allowing for different implementations (e.g., wiki page parsing, API-based).
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def validate_signature(self, signature: Signature) -> bool:
        """
        Validate a signature.

        Args:
            signature (Signature): The signature to validate

        Returns:
            bool: True if the signature is valid
        """
        pass

    @abstractmethod
    def get_signature_count(self) -> int:
        """
        Get the total count of available signatures.

        Returns:
            int: Number of available signatures
        """
        pass