# Translation Stage - LiteLLM + Google Gemini AI

This directory contains the translation stage implementation for the InfoboxSync pipeline, featuring AI-powered translation using LiteLLM and Google Gemini AI.

## Overview

The translation stage translates English Wikipedia infobox data to Arabic using advanced AI models. It follows the Strategy Pattern for extensibility and includes comprehensive error handling and fallback mechanisms.

## Architecture

### Core Components

1. **`base_translator.py`** - Abstract base classes and factory pattern
2. **`gemini_translator.py`** - Google Gemini AI implementation
3. **`config.py`** - Configuration management for API keys and settings
4. **`translate.py`** - Main translation interface and pipeline integration

### Design Patterns Used

- **Strategy Pattern**: Different translation services (Gemini, future services)
- **Factory Pattern**: Creation of appropriate translation services
- **Template Method**: Consistent translation workflow across services

## Features

### AI-Powered Translation
- Uses Google Gemini AI via LiteLLM for high-quality translations
- Supports both template-level and field-by-field translation
- Intelligent handling of different field types (text, numbers, links, images)

### Smart Field Handling
- **Text Fields**: Translated naturally while preserving meaning
- **Number Fields**: Kept in original form (heights, statistics, etc.)
- **Link Fields**: Preserved as-is with proper formatting
- **Image Fields**: Maintained without translation
- **Numbered Fields**: Translated individually while maintaining sequence

### Error Handling & Fallbacks
- Graceful degradation when API is unavailable
- Automatic fallback to field-by-field translation
- Comprehensive error logging and metadata
- Service availability checking

### Configuration Management
- Environment variable support for API keys
- Flexible configuration system
- Support for multiple API key sources

## Installation

1. Install LiteLLM:
```bash
pip install litellm
```

2. Set up your Google AI API key:
```bash
export GEMINI_API_KEY="your-google-ai-api-key-here"
# OR
export GOOGLE_AI_API_KEY="your-google-ai-api-key-here"
```

## Usage

### Basic Usage

```python
from translate.translate import translate_data

# Your mapped data from the map stage
mapped_data = {
    'page_title': 'Player Name',
    'arabic_fields': {
        'الاسم': {'value': 'John Doe', 'type': 'text'},
        'الطول': {'value': '1.80 m', 'type': 'number'},
        # ... more fields
    }
}

# Translate to Arabic (default)
result = translate_data(mapped_data)

if result['translation_metadata']['success']:
    translated_fields = result['translated_fields']
    print(f"Translated {result['translation_metadata']['translated_fields']} fields")
else:
    print(f"Translation failed: {result['translation_metadata']['error']}")
```

### Advanced Usage

```python
# Specify translation service
result = translate_data(mapped_data, service_name='gemini', target_lang='ar')

# Use field-by-field translation (alternative method)
from translate.translate import translate_field_by_field
result = translate_field_by_field(mapped_data, target_lang='ar')
```

### Service Management

```python
from translate.translate import get_available_translation_services, test_translation_service

# List available services
services = get_available_translation_services()
print(f"Available: {services}")

# Test if a service is working
is_working = test_translation_service('gemini')
print(f"Gemini available: {is_working}")
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY` - Google AI API key (preferred)
- `GOOGLE_AI_API_KEY` - Alternative Google AI API key
- `TRANSLATION_DEFAULT_SERVICE` - Default translation service ('gemini')
- `TRANSLATION_ENABLE_CACHING` - Enable/disable caching ('true'/'false')
- `TRANSLATION_CACHE_MAX_SIZE` - Maximum cache size (default: 1000)

### Configuration File

You can also use a JSON configuration file:

```json
{
  "gemini": {
    "model": "gemini/gemini-1.5-flash",
    "temperature": 0.3,
    "api_key": "your-api-key-here"
  },
  "default_service": "gemini"
}
```

```python
from translate.config import setup_translation_config
config = setup_translation_config('/path/to/config.json')
```

## Data Flow

### Input Data Structure
```python
{
    'page_title': 'English Title',
    'arabic_fields': {
        'arabic_field_name': {
            'value': 'English value',
            'type': 'text|number|link|image|numbered',
            'validation': {...}
        }
    },
    'arabic_title': 'Arabic Title'
}
```

### Output Data Structure
```python
{
    'page_title': 'English Title',
    'arabic_fields': {...},  # Original fields
    'translated_fields': {
        'arabic_field_name': {
            'value': 'English value',
            'translated_value': 'Arabic translation',
            'translation_confidence': 0.9,
            'type': 'text'
        }
    },
    'translation_metadata': {
        'service': 'Google Gemini AI',
        'target_language': 'ar',
        'translation_method': 'template_translation',
        'total_fields': 10,
        'translated_fields': 8,
        'success': True
    },
    'translated_title': 'Arabic Title'
}
```

## Translation Methods

### 1. Template Translation (Default)
- Sends entire infobox as context to AI
- Maintains relationships between fields
- More accurate for complex templates
- Better handling of numbered sequences

### 2. Field-by-Field Translation
- Translates each field individually
- Faster for simple cases
- Easier to debug
- Good fallback when template translation fails

## Prompt Engineering

The Gemini translator uses carefully crafted prompts:

### Infobox Translation Prompt
```python
prompt = f"""You are a professional translator specializing in Wikipedia infobox content.

Please translate the following infobox data from English to Arabic. The data contains field names in Arabic and their corresponding values in English.

INSTRUCTION:
- Translate ONLY the VALUES (not the Arabic field names)
- Maintain the exact structure and format
- For numbered fields (arrays), translate each item individually
- Keep technical terms, proper names, and numbers in their original form when appropriate
- Ensure the translation is natural and appropriate for Wikipedia content

FIELDS TO TRANSLATE:
{fields_text}

Please provide the translated infobox in the following JSON format:
{{
  "translated_fields": {{
    "field_name_1": "translated_value_1",
    "field_name_2": "translated_value_2",
    ...
  }},
  "translation_metadata": {{
    "total_fields": number,
    "translated_fields": number,
    "skipped_fields": number
  }}
}}

IMPORTANT: Only output valid JSON, no additional text or explanations."""
```

## Error Handling

### Common Error Scenarios

1. **Missing API Key**
   - Returns error metadata
   - Logs warning message
   - Doesn't crash the pipeline

2. **API Rate Limiting**
   - Automatic retry with exponential backoff
   - Graceful degradation to field-by-field translation

3. **Invalid JSON Response**
   - Fallback to field-by-field translation
   - Logs parsing errors for debugging

4. **Network Issues**
   - Timeout handling
   - Retry mechanisms
   - Error metadata for pipeline continuation

### Fallback Strategy

1. **Primary**: Template-level translation with Gemini
2. **Fallback 1**: Field-by-field translation with Gemini
3. **Fallback 2**: Return original data with error metadata

## Testing

Run the test script to verify functionality:

```bash
python test_translation.py
```

The test script demonstrates:
- Service availability checking
- Error handling without API keys
- Full translation workflow with API keys
- Field-by-field translation comparison

## Performance Considerations

### Caching
- Translation results can be cached to reduce API calls
- Configurable cache size and TTL
- Cache keys based on field content

### Optimization
- Batch translation for multiple fields
- Intelligent field type detection
- Minimal API calls for unchanged content

## Future Enhancements

### Additional Services
- OpenAI GPT models
- Microsoft Translator
- DeepL Pro
- Custom fine-tuned models

### Advanced Features
- Translation memory for repeated phrases
- Glossary support for domain-specific terms
- Quality scoring and confidence metrics
- Multi-language support

### Integration Improvements
- Async translation for better performance
- Streaming responses for large infoboxes
- Cost optimization and usage tracking

## Troubleshooting

### Common Issues

1. **"litellm not installed"**
   ```bash
   pip install litellm
   ```

2. **"No API key provided"**
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

3. **"Translation service not available"**
   - Check API key validity
   - Verify network connectivity
   - Check API quota/limits

4. **JSON parsing errors**
   - Usually indicates AI response format issues
   - Automatically falls back to field-by-field translation
   - Check logs for response content

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To add new translation services:

1. Create new translator class inheriting from `TranslationService`
2. Implement required abstract methods
3. Register service in factory: `TranslationServiceFactory.register_service(name, class)`
4. Add service configuration in `config.py`

Example:
```python
class CustomTranslator(TranslationService):
    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # Your implementation
        pass

# Register
TranslationServiceFactory.register_service("custom", CustomTranslator)