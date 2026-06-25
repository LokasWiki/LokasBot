import logging
from typing import Dict, Any, Optional
from .base_translator import TranslationServiceFactory
from .config import get_translation_config

logger = logging.getLogger(__name__)


def translate_data(mapped_data: dict, target_lang: str = 'ar',
                  service_name: Optional[str] = None) -> dict:
    """
    Translate the mapped data to the target language using AI translation services.

    Args:
        mapped_data (dict): The mapped data from the map stage with Arabic field names.
        target_lang (str): Target language code (default: 'ar' for Arabic).
        service_name (Optional[str]): Translation service to use. If None, uses default.

    Returns:
        dict: Translated data with additional translation metadata.
    """
    logger.info(f"Starting data translation to {target_lang}")

    try:
        # Get configuration
        config = get_translation_config()

        # Determine which service to use
        if not service_name:
            service_name = config.get_default_service()

        logger.info(f"Using translation service: {service_name}")

        # Create translation service
        try:
            translator = TranslationServiceFactory.create_service(
                service_name,
                source_lang='en',
                target_lang=target_lang
            )
        except Exception as e:
            logger.error(f"Failed to create translation service {service_name}: {e}")
            # Return original data with error metadata
            return _add_translation_error(mapped_data, str(e))

        # Check if service is available
        if not translator.is_available():
            error_msg = f"Translation service {service_name} is not available"
            logger.error(error_msg)
            return _add_translation_error(mapped_data, error_msg)

        # Extract infobox data for translation
        arabic_fields = mapped_data.get('arabic_fields', {})
        if not arabic_fields:
            logger.warning("No Arabic fields found in mapped data")
            return _add_translation_metadata(mapped_data, {}, "no_fields")

        logger.info(f"Translating {len(arabic_fields)} fields")

        # Translate the infobox data
        translation_result = translator.translate_infobox(arabic_fields)

        # Process translation results
        translated_infobox = translation_result.get('translated_infobox', {})
        translation_metadata = translation_result.get('translation_metadata', {})

        # Build the final translated data structure
        translated_data = mapped_data.copy()
        translated_data['translated_fields'] = translated_infobox
        translated_data['translation_metadata'] = {
            'service': translator.get_service_name(),
            'target_language': target_lang,
            'translation_method': translation_metadata.get('method', 'unknown'),
            'total_fields': translation_result.get('original_field_count', 0),
            'translated_fields': translation_result.get('translated_field_count', 0),
            'success': True
        }

        # Update page title if it's in English and we have an Arabic title
        if 'arabic_title' in mapped_data and mapped_data['arabic_title']:
            translated_data['translated_title'] = mapped_data['arabic_title']

        logger.info(f"Successfully translated data for: {mapped_data.get('page_title', 'Unknown')}")
        logger.info(f"Translation stats: {translation_result.get('translated_field_count', 0)}/"
                   f"{translation_result.get('original_field_count', 0)} fields translated")

        return translated_data

    except Exception as e:
        logger.error(f"Error translating data: {e}")
        return _add_translation_error(mapped_data, str(e))


def _add_translation_metadata(mapped_data: dict, translation_metadata: dict,
                             method: str = "unknown") -> dict:
    """Add translation metadata to mapped data."""
    translated_data = mapped_data.copy()
    translated_data['translation_metadata'] = {
        'service': 'unknown',
        'target_language': 'ar',
        'translation_method': method,
        'success': True,
        **translation_metadata
    }
    return translated_data


def _add_translation_error(mapped_data: dict, error_message: str) -> dict:
    """Add translation error metadata to mapped data."""
    translated_data = mapped_data.copy()
    translated_data['translation_metadata'] = {
        'service': 'unknown',
        'target_language': 'ar',
        'success': False,
        'error': error_message
    }
    return translated_data


def get_available_translation_services() -> list:
    """
    Get list of available translation services.

    Returns:
        list: List of available service names
    """
    try:
        return TranslationServiceFactory.get_available_services()
    except Exception as e:
        logger.error(f"Error getting available services: {e}")
        return []


def test_translation_service(service_name: str = 'gemini') -> bool:
    """
    Test if a translation service is available and working.

    Args:
        service_name (str): Name of the service to test

    Returns:
        bool: True if service is available and working
    """
    try:
        config = get_translation_config()
        if not config.has_api_key(service_name):
            logger.warning(f"No API key available for {service_name}")
            return False

        translator = TranslationServiceFactory.create_service(service_name)
        return translator.is_available()
    except Exception as e:
        logger.error(f"Error testing translation service {service_name}: {e}")
        return False


def translate_field_by_field(mapped_data: dict, target_lang: str = 'ar',
                           service_name: Optional[str] = None) -> dict:
    """
    Translate data field by field (alternative to template-based translation).

    Args:
        mapped_data (dict): The mapped data from the map stage.
        target_lang (str): Target language code.
        service_name (Optional[str]): Translation service to use.

    Returns:
        dict: Translated data with field-by-field results.
    """
    logger.info(f"Starting field-by-field translation to {target_lang}")

    try:
        # Get configuration and create translator (same as main function)
        config = get_translation_config()
        if not service_name:
            service_name = config.get_default_service()

        translator = TranslationServiceFactory.create_service(
            service_name,
            source_lang='en',
            target_lang=target_lang
        )

        if not translator.is_available():
            return _add_translation_error(mapped_data, f"Service {service_name} not available")

        arabic_fields = mapped_data.get('arabic_fields', {})
        translated_fields = {}

        # Translate each field individually
        for arabic_key, field_data in arabic_fields.items():
            if isinstance(field_data, dict) and 'value' in field_data:
                field_type = field_data.get('type', 'text')
                value = field_data.get('value', '')

                # Skip certain field types
                if field_type in ['number', 'link', 'image']:
                    translated_fields[arabic_key] = field_data
                    continue

                # Translate the field value
                translation_result = translator.translate_field(arabic_key, value)

                if translation_result.confidence > 0:
                    new_field_data = field_data.copy()
                    new_field_data['translated_value'] = translation_result.translated_text
                    new_field_data['translation_confidence'] = translation_result.confidence
                    translated_fields[arabic_key] = new_field_data
                else:
                    translated_fields[arabic_key] = field_data

        # Build final result
        translated_data = mapped_data.copy()
        translated_data['translated_fields'] = translated_fields
        translated_data['translation_metadata'] = {
            'service': translator.get_service_name(),
            'target_language': target_lang,
            'translation_method': 'field_by_field',
            'total_fields': len(arabic_fields),
            'translated_fields': len([k for k, v in translated_fields.items()
                                     if isinstance(v, dict) and 'translated_value' in v]),
            'success': True
        }

        logger.info("Field-by-field translation completed")
        return translated_data

    except Exception as e:
        logger.error(f"Error in field-by-field translation: {e}")
        return _add_translation_error(mapped_data, str(e))