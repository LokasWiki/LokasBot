"""
Configuration layer package.

This package contains configuration management components that handle
externalized settings, templates, and application configuration.
It follows the Clean Architecture principle of keeping configuration
separate from business logic.
"""

from .config_loader import ConfigLoader

__all__ = ['ConfigLoader']