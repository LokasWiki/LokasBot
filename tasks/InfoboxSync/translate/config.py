"""
Configuration for translation services.
"""

import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TranslationConfig:
    """Configuration manager for translation services."""

    # Default configuration
    DEFAULT_CONFIG = {
        'gemini': {
            'model': 'gemini/gemini-2.0-flash',
            'temperature': 0.3,
            # 'max_tokens': 2000,
            'api_key_env_vars': ['GEMINI_API_KEY', 'GOOGLE_AI_API_KEY']
        },
        'default_service': 'gemini',
        'fallback_service': None,
        'enable_caching': True,
        'cache_max_size': 1000,
        'request_timeout': 30,
        'retry_attempts': 3,
        'retry_delay': 1.0
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file (Optional[str]): Path to configuration file
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_from_env()
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # API Keys
        for service, service_config in self.config.items():
            if isinstance(service_config, dict) and 'api_key_env_vars' in service_config:
                for env_var in service_config['api_key_env_vars']:
                    api_key = os.getenv(env_var)
                    if api_key:
                        self.config[service]['api_key'] = api_key
                        logger.info(f"Loaded API key for {service} from {env_var}")
                        break

        # Other environment variables
        if os.getenv('TRANSLATION_DEFAULT_SERVICE'):
            self.config['default_service'] = os.getenv('TRANSLATION_DEFAULT_SERVICE')

        if os.getenv('TRANSLATION_ENABLE_CACHING') == 'false':
            self.config['enable_caching'] = False

        if os.getenv('TRANSLATION_CACHE_MAX_SIZE'):
            try:
                self.config['cache_max_size'] = int(os.getenv('TRANSLATION_CACHE_MAX_SIZE'))
            except ValueError:
                pass

    def _load_from_file(self, config_file: str):
        """Load configuration from file."""
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self._merge_config(file_config)
                logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.warning(f"Failed to load configuration from {config_file}: {e}")

    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration with existing."""
        for key, value in new_config.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value

    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """Get configuration for a specific service."""
        return self.config.get(service_name, {})

    def get_default_service(self) -> str:
        """Get default translation service."""
        return self.config['default_service']

    def has_api_key(self, service_name: str) -> bool:
        """Check if API key is available for service."""
        service_config = self.get_service_config(service_name)
        return 'api_key' in service_config and service_config['api_key']

    def get_api_key(self, service_name: str) -> Optional[str]:
        """Get API key for service."""
        service_config = self.get_service_config(service_name)
        return service_config.get('api_key')


# Global configuration instance
translation_config = TranslationConfig()


def get_translation_config() -> TranslationConfig:
    """Get global translation configuration."""
    return translation_config


def setup_translation_config(config_file: Optional[str] = None) -> TranslationConfig:
    """Setup translation configuration."""
    global translation_config
    translation_config = TranslationConfig(config_file)
    return translation_config