"""
Google Gemini AI translation service using LiteLLM.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from .base_translator import TranslationService, TranslationResult, TranslationServiceFactory

logger = logging.getLogger(__name__)


class GeminiTranslator(TranslationService):
    """Google Gemini AI translation service using LiteLLM."""

    def __init__(self,
                 api_key: Optional[str] = None,
                 model: str = "gemini/gemini-2.0-flash",
                 source_lang: str = 'en',
                 target_lang: str = 'ar',
                 temperature: float = 0.3,
                 max_tokens: int = 5000):
        """
        Initialize Gemini translator.

        Args:
            api_key (Optional[str]): Google AI API key. If None, uses GEMINI_API_KEY env var
            model (str): Gemini model to use
            source_lang (str): Source language code
            target_lang (str): Target language code
            temperature (float): Sampling temperature
            max_tokens (int): Maximum tokens in response
        """
        super().__init__(source_lang, target_lang)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY')
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            logger.warning("No API key provided for Gemini translator")

        # Import litellm here to avoid import errors if not installed
        try:
            import litellm
            self.litellm = litellm
        except ImportError:
            logger.error("litellm not installed. Install with: pip install litellm")
            raise ImportError("litellm is required for GeminiTranslator")

    def _load_prompt_template(self) -> str:
        """Load the prompt template from file."""
        template_path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt template not found at {template_path}, using default template")
            return self._get_default_prompt_template()
        except Exception as e:
            logger.warning(f"Error loading prompt template: {e}, using default template")
            return self._get_default_prompt_template()

    def _get_default_prompt_template(self) -> str:
        """Get default prompt template if file is not available."""
        return """You are a professional translator specializing in Wikipedia infobox content.

Translate ALL the following field values from English to Arabic in ONE SINGLE REQUEST. Each field is marked with [index] for identification.

INSTRUCTION:
- Translate EVERY field value to Arabic
- Keep the [index] markers in your response
- Translate naturally while maintaining meaning
- Keep technical terms, proper names, and numbers in original form when appropriate
- For numbered field items, translate each one individually
- Output in the SAME format with [index] markers

FIELDS TO TRANSLATE:
{{FIELDS_TEXT}}

RESPONSE FORMAT:
[{{START_INDEX}}]: translated_value_1
[{{START_INDEX+1}}]: translated_value_2
[{{START_INDEX+2}}]: translated_value_3
...continue for all fields...

IMPORTANT: Respond with ALL translated fields using the SAME [index] markers."""

    def _build_prompt_from_template(self, template: str, fields_text: str, start_index: int = 0) -> str:
        """Build prompt by replacing placeholders in template."""
        # Replace placeholders
        prompt = template.replace('{{FIELDS_TEXT}}', fields_text)
        prompt = prompt.replace('{{START_INDEX}}', str(start_index))
        prompt = prompt.replace('{{START_INDEX+1}}', str(start_index + 1))
        prompt = prompt.replace('{{START_INDEX+2}}', str(start_index + 2))

        return prompt

    def _get_infobox_translation_prompt(self, infobox_data: Dict[str, Any]) -> tuple[str, dict]:
        """Generate prompt for single-request infobox translation and return field mapping."""
        # Extract field information and prepare for single translation request
        fields_list = []
        field_mapping = {}  # Map field index to arabic key

        for idx, (arabic_key, field_data) in enumerate(infobox_data.items()):
            if isinstance(field_data, dict) and 'value' in field_data:
                value = field_data['value']
                field_type = field_data.get('type', 'text')

                # Handle different field types
                if field_type == 'numbered' and isinstance(value, list):
                    # For numbered fields, prepare each item for translation
                    for i, item in enumerate(value):
                        fields_list.append(f"[{idx}_{i}]: {item}")
                        field_mapping[f"{idx}_{i}"] = (arabic_key, i)
                elif field_type in ['number', 'link', 'image']:
                    # Skip translation for these field types, but keep mapping for reference
                    field_mapping[str(idx)] = (arabic_key, None)
                else:
                    fields_list.append(f"[{idx}]: {value}")
                    field_mapping[str(idx)] = (arabic_key, None)

        fields_text = '\n'.join(fields_list)

        # Load template and build prompt
        template = self._load_prompt_template()
        prompt = self._build_prompt_from_template(template, fields_text, start_index=0)

        return prompt, field_mapping

    def _parse_single_request_response(self, response_text: str, field_mapping: dict) -> Dict[str, Any]:
        """Parse the single-request translation response and map back to fields."""
        translated_fields = {}

        # Parse response line by line
        lines = response_text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for [index]: translated_value pattern
            if line.startswith('[') and ']:' in line:
                try:
                    index_end = line.find(']:')
                    index = line[1:index_end].strip()
                    translated_value = line[index_end + 2:].strip()

                    if index in field_mapping:
                        arabic_key, item_index = field_mapping[index]

                        if arabic_key not in translated_fields:
                            translated_fields[arabic_key] = {}

                        if item_index is not None:
                            # This is part of a numbered field
                            if 'value' not in translated_fields[arabic_key]:
                                translated_fields[arabic_key]['value'] = []
                            translated_fields[arabic_key]['value'].append(translated_value)
                        else:
                            # This is a single field
                            translated_fields[arabic_key]['value'] = translated_value

                except (ValueError, IndexError) as e:
                    logger.warning(f"Failed to parse response line: {line} - {e}")
                    continue

        return translated_fields

    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Translate an entire infobox template in ONE SINGLE REQUEST."""
        try:
            logger.info(f"Starting single-request infobox translation with {len(infobox_data)} fields")

            # Generate single-request prompt and field mapping
            prompt, field_mapping = self._get_infobox_translation_prompt(infobox_data)

            # Make single API call for all fields
            response_text = self._call_gemini(prompt)

            # Parse the single response
            translated_fields = self._parse_single_request_response(response_text, field_mapping)

            # Merge translated fields back into original structure
            translated_infobox = {}
            for arabic_key, field_data in infobox_data.items():
                if arabic_key in translated_fields:
                    # Create new field data with translated value
                    new_field_data = field_data.copy()
                    new_field_data['translated_value'] = translated_fields[arabic_key]['value']
                    new_field_data['translation_confidence'] = 0.9
                    translated_infobox[arabic_key] = new_field_data
                else:
                    # Keep original if not translated
                    translated_infobox[arabic_key] = field_data

            logger.info(f"Successfully translated infobox with {len(translated_fields)} fields in ONE request")

            return {
                'translated_infobox': translated_infobox,
                'translation_metadata': {
                    'method': 'single_request',
                    'api_calls': 1,
                    'total_fields': len(infobox_data),
                    'translated_fields': len(translated_fields)
                },
                'original_field_count': len(infobox_data),
                'translated_field_count': len(translated_fields)
            }

        except Exception as e:
            logger.error(f"Single-request infobox translation failed: {e}")
            # Return original data with error metadata
            return {
                'translated_infobox': infobox_data,
                'translation_metadata': {
                    'method': 'single_request_failed',
                    'error': str(e),
                    'api_calls': 0
                },
                'original_field_count': len(infobox_data),
                'translated_field_count': 0
            }

    def _call_gemini(self, prompt: str) -> str:
        """Make API call to Gemini via LiteLLM."""
        try:
            response = self.litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise

    def translate_text(self, text: str, **kwargs) -> TranslationResult:
        """Translate a single text string."""
        try:
            prompt = f"Translate the following text from {self.source_lang} to {self.target_lang}:\n\n{text}\n\nTranslation:"
            translated_text = self._call_gemini(prompt).strip()

            return TranslationResult(
                translated_text=translated_text,
                original_text=text,
                confidence=0.9,
                metadata={"model": self.model, "method": "single_text"}
            )
        except Exception as e:
            logger.error(f"Text translation failed: {e}")
            return TranslationResult(
                translated_text=text,
                original_text=text,
                confidence=0.0,
                metadata={"error": str(e)}
            )

    def translate_field(self, field_name: str, field_value: Any, **kwargs) -> TranslationResult:
        """Translate a field name and value pair."""
        try:
            # Skip translation for certain field types
            if isinstance(field_value, dict):
                field_type = field_value.get('type', 'text')
                value = field_value.get('value', '')

                # Don't translate numbers, links, or images
                if field_type in ['number', 'link', 'image']:
                    return TranslationResult(
                        translated_text=str(value),
                        original_text=str(value),
                        confidence=1.0,
                        metadata={"skipped": True, "reason": f"field_type_{field_type}"}
                    )
            else:
                value = field_value

            prompt = f"""Translate the following field value to Arabic:

Field: {field_name}
Value: {value}
Type: text

INSTRUCTION:
- Translate naturally and maintain meaning
- Keep technical terms and proper names in original form when appropriate
- Output only the translated text, no explanations

Translated value:"""

            translated_text = self._call_gemini(prompt).strip()

            return TranslationResult(
                translated_text=translated_text,
                original_text=str(value),
                confidence=0.9,
                metadata={"model": self.model, "method": "field_translation"}
            )
        except Exception as e:
            logger.error(f"Field translation failed for {field_name}: {e}")
            return TranslationResult(
                translated_text=str(field_value),
                original_text=str(field_value),
                confidence=0.0,
                metadata={"error": str(e)}
            )

    def is_available(self) -> bool:
        """Check if Gemini service is available."""
        if not self.api_key:
            return False

        try:
            # Try a simple test call
            test_prompt = "Say 'OK' if you can understand this message."
            response = self._call_gemini(test_prompt)
            return 'OK' in response.upper()
        except Exception:
            return False

    def get_service_name(self) -> str:
        """Get service name."""
        return "Google Gemini AI"


# Register the service
TranslationServiceFactory.register_service("gemini", GeminiTranslator)
TranslationServiceFactory.register_service("google_gemini", GeminiTranslator)