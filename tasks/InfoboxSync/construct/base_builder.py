"""
Base template builder classes following Strategy Pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class BuildResult:
    """Result of a template building operation."""
    template_text: str
    template_type: str
    field_count: int
    success: bool
    metadata: Dict[str, Any]
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class TemplateBuilder(ABC):
    """Abstract base class for template builders."""

    def __init__(self, template_type: str = 'generic'):
        self.template_type = template_type

    @abstractmethod
    def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult:
        """
        Build a Wikipedia template from translated data.

        Args:
            translated_data (Dict[str, Any]): Translated data with Arabic field names
            **kwargs: Additional parameters for building

        Returns:
            BuildResult: Template building result
        """
        pass

    @abstractmethod
    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        """
        Format a single field for the template.

        Args:
            arabic_key (str): Arabic field name
            field_data (Dict[str, Any]): Field data with value and type

        Returns:
            str: Formatted field string
        """
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        """
        Get the Wikipedia template name for this builder.

        Returns:
            str: Template name (e.g., 'infobox football biography')
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this builder is available and properly configured."""
        pass

    @abstractmethod
    def get_builder_name(self) -> str:
        """Get the name of this builder."""
        pass


class TemplateBuilderFactory:
    """Factory for creating template builders."""

    _builders = {}

    @classmethod
    def register_builder(cls, builder_name: str, builder_class):
        """Register a new template builder."""
        cls._builders[builder_name] = builder_class

    @classmethod
    def create_builder(cls, builder_name: str, **kwargs) -> TemplateBuilder:
        """
        Create a template builder instance.

        Args:
            builder_name (str): Name of the builder to create
            **kwargs: Parameters for builder initialization

        Returns:
            TemplateBuilder: Builder instance

        Raises:
            ValueError: If builder is not registered or creation fails
        """
        if builder_name not in cls._builders:
            available_builders = list(cls._builders.keys())
            raise ValueError(f"Unknown template builder: {builder_name}. "
                           f"Available builders: {available_builders}")

        builder_class = cls._builders[builder_name]
        try:
            return builder_class(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create {builder_name} builder: {e}")

    @classmethod
    def get_available_builders(cls) -> List[str]:
        """Get list of available template builders."""
        return list(cls._builders.keys())

    @classmethod
    def get_supported_template_types(cls) -> List[str]:
        """Get list of supported template types across all builders."""
        template_types = []
        for builder_class in cls._builders.values():
            try:
                # Create a temporary instance to get template name
                temp_builder = builder_class()
                template_types.append(temp_builder.get_template_name())
            except Exception:
                continue
        return template_types