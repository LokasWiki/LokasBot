"""
Base translation service interface following Strategy Pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class TranslationResult:
    """Result of a translation operation."""

    def __init__(self,
                 translated_text: str,
                 original_text: str,
                 confidence: float = 1.0,
                 metadata: Optional[Dict[str, Any]] = None):
        self.translated_text = translated_text
        self.original_text = original_text
        self.confidence = confidence
        self.metadata = metadata or {}


class TranslationService(ABC):
    """Abstract base class for translation services."""

    def __init__(self, source_lang: str = 'en', target_lang: str = 'ar'):
        self.source_lang = source_lang
        self.target_lang = target_lang

    @abstractmethod
    def translate_text(self, text: str, **kwargs) -> TranslationResult:
        """
        Translate a single text string.

        Args:
            text (str): Text to translate
            **kwargs: Additional parameters for translation

        Returns:
            TranslationResult: Translation result
        """
        pass

    @abstractmethod
    def translate_field(self, field_name: str, field_value: Any, **kwargs) -> TranslationResult:
        """
        Translate a field name and value pair.

        Args:
            field_name (str): Name of the field
            field_value (Any): Value of the field
            **kwargs: Additional parameters

        Returns:
            TranslationResult: Translation result
        """
        pass

    @abstractmethod
    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Translate an entire infobox template.

        Args:
            infobox_data (Dict[str, Any]): Infobox data with Arabic field names
            **kwargs: Additional parameters

        Returns:
            Dict[str, Any]: Translated infobox data
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the translation service is available and properly configured."""
        pass

    @abstractmethod
    def get_service_name(self) -> str:
        """Get the name of this translation service."""
        pass


class TranslationServiceFactory:
    """Factory for creating translation services."""

    _services = {}

    @classmethod
    def register_service(cls, service_name: str, service_class):
        """Register a new translation service."""
        cls._services[service_name] = service_class

    @classmethod
    def create_service(cls, service_name: str, **kwargs) -> TranslationService:
        """
        Create a translation service instance.

        Args:
            service_name (str): Name of the service to create
            **kwargs: Parameters for service initialization

        Returns:
            TranslationService: Service instance

        Raises:
            ValueError: If service is not registered or creation fails
        """
        if service_name not in cls._services:
            available_services = list(cls._services.keys())
            raise ValueError(f"Unknown translation service: {service_name}. "
                           f"Available services: {available_services}")

        service_class = cls._services[service_name]
        try:
            return service_class(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create {service_name} service: {e}")

    @classmethod
    def get_available_services(cls) -> List[str]:
        """Get list of available translation services."""
        return list(cls._services.keys())